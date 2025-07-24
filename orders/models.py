from django.db import models
from django.contrib.auth import get_user_model
from event.models import Activity
from decimal import Decimal

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.activity.name}"

class OrderItem(models.Model):
    TICKET_TYPES = [
        ('standart', 'Tam'),
        ('student', 'Öğrenci'),
        ('vip', 'VIP'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES)
    quantity = models.PositiveIntegerField()

    def get_price(self):
        base_price = self.order.activity.ticket_price
        multiplier = {
            'standart': Decimal('1.0'),
            'student': Decimal('0.8'),
            'vip': Decimal('1.5')
        }.get(self.ticket_type, Decimal('1.0'))

        return base_price * self.quantity * multiplier





    
   
    
   
    
   
