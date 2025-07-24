from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from constance import config
from django.template import Template, Context

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

    
    @staticmethod
    def register_mail(user):
        template_value = {
            "first_name" : user.first_name
        }
        template_val = Context(template_value)
        email_message = Template(config.REGISTER_MAIL_TEMPLATE).render(template_val)
        from_email = config.FROM_EMAIL
        subject = "Hesabınız başarıyla oluşturuldu."
        recipient_list = [user.email]
    
        send_mail(
            subject=subject,
            message=email_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
            html_message=email_message
        )

    @staticmethod
    def login_mail(user):
        template_value = {
            "first_name": user.first_name
        }
        template_val = Context(template_value)
        email_message = Template(config.LOGIN_MAIL_TEMPLATE).render(template_val)

        subject = "Hesabınıza başarıyla giriş yapıldı."

        from_email = config.FROM_EMAIL
        recipient_list = [user.email] 

        send_mail(
            subject=subject,
            message=email_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
            html_message=email_message
        )
