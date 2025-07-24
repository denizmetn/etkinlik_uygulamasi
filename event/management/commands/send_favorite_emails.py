from django.core.management.base import BaseCommand
from django.utils.timezone import now, make_aware
from datetime import datetime, time, timedelta
from django.core.mail import send_mail
from django.template import Template, Context
from constance import config
from event.models import Favorite

class Command(BaseCommand):
    help = "Favori etkinlikleri yaklaşan kullanıcılara e-posta gönderir."

    def handle(self, *args, **kwargs):
        reminder_date = now() + timedelta(days=1)
        start_of_day = make_aware(datetime.combine(reminder_date.date(), time.min))
        end_of_day = make_aware(datetime.combine(reminder_date.date(), time.max))

        favorites = Favorite.objects.filter(
            activity__start_date__range=(start_of_day, end_of_day)
        ).select_related('user', 'activity')

        for fav in favorites:
            user = fav.user
            activity = fav.activity
            
            context = {
                "first_name" : user.first_name,
                "event_title" : activity.name,
                "event_start" : activity.start_date.strftime("%d %B %Y, %H:%M"),
            }
            template = Template(config.FAVORITE_MAIL_TEMPLATE)
            email_message = template.render(Context(context))
            
            subject = f"Yaklaşan favoriniz: {context['event_title']}"
            from_email = config.FROM_EMAIL
            recipient_list = [user.email]
            
            send_mail(
                subject=subject,
                message=email_message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
                html_message=email_message,
            )
            self.stdout.write(f"Mail gönderildi: {user.email} - {activity.name}")
                
        
