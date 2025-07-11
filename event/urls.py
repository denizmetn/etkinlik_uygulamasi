from django.urls import path
from .import views


app_name = "event"

urlpatterns = [
    path("",views.activity_list, name="home"),
    path("<slug:slug>/",views.activity_detail,name="activity_detail")

]