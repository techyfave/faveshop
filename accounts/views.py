# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_http_methods

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

# Handle both GET and POST for logout
def logout_view(request):
    logout(request)
    return redirect('home')



# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
    
#     return render(request, 'accounts/register.html', {'form': form})

# @login_required
# def profile(request):
#     return render(request, 'accounts/profile.html')