import json
from iyzipay import CheckoutFormInitialize
import uuid
from django.conf import settings

def create_payment_request(order, callback_url):
    print(f"Order total price: {order.total_price}") 
    conversation_id = str(uuid.uuid4()) 
    
    request_data = {
        "locale": "tr",
        "conversationId": conversation_id,
        "price": str(order.total_price),
        "paidPrice": str(order.total_price),
        "currency": "TRY",
        "basketId": str(order.id),
        "paymentGroup": "PRODUCT",
        "callbackUrl": callback_url,
        "enabledInstallment": [1, 2, 3],
        "buyer": {
            "id": str(order.user.id),
            "name": order.user.first_name or "Ad",
            "surname": order.user.last_name or "Soyad",
            "email": order.user.email or "eposta@example.com",
            "identityNumber": "11111111111",
            "registrationAddress": "Test Adresi, İstanbul",  
            "city": "İstanbul",
            "country": "Türkiye",
            "zipCode": "34000",
            "ip": "85.34.78.112"
        },

        "shippingAddress": {
            "contactName": f"{order.user.first_name or 'Ad'} {order.user.last_name or 'Soyad'}",
            "city": "İstanbul",
            "country": "Türkiye",
            "address": "Varsayılan Adres",
            "zipCode": "34000"
        },
        "billingAddress": {
            "contactName": f"{order.user.first_name or 'Ad'} {order.user.last_name or 'Soyad'}",
            "city": "İstanbul",
            "country": "Türkiye",
            "address": "Varsayılan Adres",
            "zipCode": "34000"
        },
        "basketItems": [{
            "id": str(order.id),
            "name": order.activity.name,
            "category1": order.activity.category.name,
            "itemType": "VIRTUAL",
            "price": str(order.total_price)
        }]
    }
    
    options = {
        "api_key": settings.IYZICO_API_KEY,
        "secret_key": settings.IYZICO_SECRET_KEY,
        "base_url": settings.IYZICO_BASE_URL,
    }
    checkout_form_initialize = CheckoutFormInitialize()
    response = checkout_form_initialize.create(request_data, options)
    response_json = json.loads(response.read().decode("utf-8"))
    print("İYZİCO DÖNEN CEVAP:")
    print(json.dumps(response_json, indent=2, ensure_ascii=False))
    return response_json



   

