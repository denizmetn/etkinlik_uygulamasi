from django.shortcuts import render,get_object_or_404
from .models import Activity


def activity_list(request):
    activities = Activity.objects.all()
    context = {
        "activities" : activities # soldaki HTML şablonunda kullanılacak isim, sağdaki veritabanından çekilen etkinlik listesidir.

    }
    return render(request, "event/activity_list.html", context)


def activity_detail(request, slug):
    activity = get_object_or_404(Activity, slug=slug)
    context = {
        "activity" : activity
    }
    return render(request, "event/activity_detail.html", context)



