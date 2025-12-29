import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderForm

@login_required
def order_create(request):
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.error(request, 'Your cart is empty')
        return redirect('cart_detail')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            
            if request.user.is_authenticated:
                order.user = request.user
            
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Clear the cart
            cart.clear()
            
            return redirect('order_created', order_id=order.id)
    else:
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
            form = OrderForm(initial=initial_data)
        else:
            form = OrderForm()
    
    return render(request, 'orders/create.html', {
        'cart': cart,
        'form': form,
    })

def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/created.html', {'order': order})

def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Convert amount to kobo (Paystack uses kobo)
    amount = int(order.total_amount * 100)
    
    # Prepare payment data
    payment_data = {
        'email': order.email,
        'amount': amount,
        'reference': f'order_{order.id}_{order.created_at.timestamp()}',
        'callback_url': request.build_absolute_uri('/orders/payment/callback/'),
        'metadata': {
            'order_id': order.id,
            'custom_fields': [
                {
                    'display_name': 'Order ID',
                    'variable_name': 'order_id',
                    'value': order.id
                }
            ]
        }
    }
    
    # Headers for Paystack API
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            headers=headers,
            json=payment_data
        )
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data['status']:
                # Save payment reference
                order.payment_reference = response_data['data']['reference']
                order.save()
                
                # Redirect to Paystack payment page
                return redirect(response_data['data']['authorization_url'])
            else:
                messages.error(request, 'Failed to initialize payment')
                return redirect('order_created', order_id=order.id)
        else:
            messages.error(request, 'Payment service error')
            return redirect('order_created', order_id=order.id)
    
    except Exception as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('order_created', order_id=order.id)

@csrf_exempt
def payment_callback(request):
    if request.method == 'GET':
        reference = request.GET.get('reference')
        
        if reference:
            # Verify payment with Paystack
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            }
            
            try:
                response = requests.get(
                    f'https://api.paystack.co/transaction/verify/{reference}',
                    headers=headers
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    
                    if response_data['data']['status'] == 'success':
                        # Find order by reference
                        order = Order.objects.filter(payment_reference=reference).first()
                        
                        if order:
                            order.paid = True
                            order.status = 'processing'
                            order.save()
                            
                            messages.success(request, 'Payment successful! Your order is being processed.')
                            return redirect('order_created', order_id=order.id)
                
                messages.error(request, 'Payment verification failed')
                return redirect('home')
            
            except Exception as e:
                messages.error(request, f'Payment verification error: {str(e)}')
                return redirect('home')
    
    messages.error(request, 'Invalid request')
    return redirect('home')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})