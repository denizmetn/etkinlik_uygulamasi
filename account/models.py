from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('attendee','Katılımcı'),
        ('organizer', 'Organizatör'),
        ('admin','Yönetici')
    )

    role = models.CharField(max_length =20, choices=ROLE_CHOICES, default ='attendee')

    def __str__ (self):
        return self.username

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = "Kullanıcılar"    

