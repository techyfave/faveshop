from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('created/<int:order_id>/', views.order_created, name='order_created'),
    path('payment/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('history/', views.order_history, name='order_history'),
]