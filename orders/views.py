import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from event.models import Activity
from .models import Order, OrderItem
from .forms import OrderForm
from django.urls import reverse
from iyzipay import Payment, CheckoutForm 
from .payments import create_payment_request
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import iyzipay 


iyzipay.api_key = settings.IYZICO_API_KEY
iyzipay.secret_key = settings.IYZICO_SECRET_KEY
iyzipay.base_url = settings.IYZICO_BASE_URL

@login_required
def create_order(request, activity_slug):
    activity = get_object_or_404(Activity, slug=activity_slug)
    ticket_base_price = activity.ticket_price
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                activity=activity,
                is_paid=False,
                total_price=0
            )

            total_price = 0
            quantities = {
                'standart': form.cleaned_data['quantity_standart'],
                'student': form.cleaned_data['quantity_student'],
                'vip': form.cleaned_data['quantity_vip']
            }

            for ticket_type, qty in quantities.items():
                if qty > 0:
                    item = OrderItem.objects.create(
                        order=order,
                        ticket_type=ticket_type,
                        quantity=qty
                    )
                    total_price += item.get_price()

            order.total_price = total_price
            order.save()

            return redirect('orders:payment', order_id=order.id)
    
    context = {
        'activity': activity,
        'form': form,
        'ticket_prices': {
        'standart': float(ticket_base_price),
        'student': float(ticket_base_price * Decimal('0.8')),
        'vip': float(ticket_base_price * Decimal('1.5')),
    }
    }
    return render(request, 'orders/create_order.html', context)

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    callback_url = request.build_absolute_uri(reverse('orders:payment_callback', kwargs={'order_id': order.id}))
    
    payment_response = create_payment_request(order, callback_url)
    
    if payment_response['status'] == 'success': 
        checkout_form_content = payment_response['checkoutFormContent']
        return render(request, 'orders/payment.html', {'checkout_form': checkout_form_content})
    else:
        messages.error(request, "Ödeme işlemi başlatılamadı")
        return redirect('orders:create_order', activity_slug=order.activity.slug)


@csrf_exempt
def payment_callback(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    token = request.GET.get('token') or request.POST.get('token')
    if not token:
        messages.error(request, "Ödeme doğrulaması için gerekli token bulunamadı.")
        return render(request, 'orders/payment_failed.html', {'order': order})

    options_dict = {
        'api_key': settings.IYZICO_API_KEY,
        'secret_key': settings.IYZICO_SECRET_KEY,
        'base_url': settings.IYZICO_BASE_URL,
    }

    iyzico_request_data = {
        "locale": "tr",
        "conversationId": str(order.id), 
        "token": token, 
    }
    
    checkout_form_client = CheckoutForm() 
    http_response = checkout_form_client.retrieve(iyzico_request_data, options_dict) 

 
    try:
        response_data = json.loads(http_response.read().decode('utf-8'))
    except json.JSONDecodeError as e:
        print(f"Iyzico yanıtı JSON olarak ayrıştırılamadı: {e}")
        messages.error(request, "Ödeme yanıtı işlenirken bir hata oluştu.")
        return render(request, 'orders/payment_failed.html', {'order': order})

    
    if response_data.get('status') == 'success': 
        order.is_paid = True
        order.save()
        messages.success(request, "Ödeme başarıyla tamamlandı!")
        return render(request, 'orders/payment_success.html', {'order': order})
    else:
        error_message = response_data.get('errorMessage', 'Bilinmeyen bir hata oluştu.')
        print(f"Iyzico Ödeme Geri Çağrı Hatası: {error_message}")
        messages.error(request, f"Ödeme doğrulanamadı: {error_message}")
        return render(request, 'orders/payment_failed.html', {'order': order})