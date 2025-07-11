from django.contrib import admin

# Register your models here.
from event.models import *
admin.site.register(Activity)
admin.site.register(Township)
admin.site.register(City)
admin.site.register(Category)
admin.site.register(Location)