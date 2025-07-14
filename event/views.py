from django.shortcuts import render,get_object_or_404
from .models import Activity, Category, City
from django.utils.timezone import make_aware
from datetime import datetime, time
from django.db.models import Q 
from django.core.paginator import Paginator

def activity_list(request):
    activities = Activity.objects.all()

    category_slug = request.GET.get("category")
    city_slug = request.GET.get("city")
    date_str = request.GET.get("date")
    is_free_str = request.GET.get("is_free")

    if category_slug:
        activities = activities.filter(category__slug=category_slug)

    if city_slug:
        activities = activities.filter(township__city__slug=city_slug)

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_of_day = make_aware(datetime.combine(selected_date, time.min))
            end_of_day = make_aware(datetime.combine(selected_date, time.max))

            activities = activities.filter(
                start_date__lte=end_of_day,
                end_date__gte=start_of_day
            )
        except ValueError:
            selected_date = None

    if is_free_str == "free":
        activities = activities.filter(is_free = True)
    else:
        activities = activities.filter(is_free = False)


    search_query = request.GET.get("search","").strip()
    if search_query:
        activities = activities.filter(
            Q(name__icontains=search_query) |
            Q(location__name__icontains=search_query)  # location_name değil location__name
        )



    paginator = Paginator(activities,20)
    page_number = request.GET.get("page")
    page_obj  = paginator.get_page(page_number)

    context = {
        "activities": page_obj, # soldaki HTML şablonunda kullanılacak isim, sağdaki veritabanından çekilen etkinlik listesidir.
        "selected_category": category_slug,
        "selected_city": city_slug,
        "selected_date": date_str,
        "selected_is_free": is_free_str,
        "search_query": search_query,
        "categories": Category.objects.all(),
        "cities": City.objects.all(),
        'page_obj': page_obj,
    }    
       
    return render(request, "event/activity_list.html", context)


def activity_detail(request, slug):
    activity = get_object_or_404(Activity, slug=slug)
    context = {
        "activity" : activity
    }
    return render(request, "event/activity_detail.html", context)



