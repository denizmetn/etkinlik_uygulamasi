from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/<slug:activity_slug>', views.create_order, name='create_order'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment-callback/<int:order_id>/',views.payment_callback, name='payment_callback'),
]