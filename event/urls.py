from django.urls import path
from .import views


app_name = "event"

urlpatterns = [
    path("",views.activity_list, name="home"),
    path("<slug:slug>/",views.activity_detail,name="activity_detail"),
    path('organizer/events/new/', views.create_activity, name='create_activity'),
    path('organizer/my-events/', views.my_activities, name='my_activities'),
    path('organizer/events/edit/<slug:slug>/',views.edit_activity, name='edit_activity'),
    path('organizer/events/delete/<slug:slug>/', views.delete_activity, name='delete_activity')
]