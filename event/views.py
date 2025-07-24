from django.shortcuts import render, redirect, get_object_or_404 
from .models import Activity, Category, City, Location, Township , Favorite
from django.utils.timezone import make_aware
from datetime import datetime, time
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.urls import reverse_lazy 
from .forms import ActivityForm
from account.decorators import role_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Exists, OuterRef, Value, BooleanField



def activity_list(request):
    activities = Activity.objects.filter(is_published=True)

    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user, activity=OuterRef('pk'))
        activities = activities.annotate(is_favorite=Exists(user_favorites))
    else:
        activities = activities.annotate(is_favorite=Value(False, output_field=BooleanField()))


    category_slug = request.GET.get("category")
    city_slug = request.GET.get("city")
    date_str = request.GET.get("date")
    is_free_str = request.GET.get("is_free")

    activities = activities.filter(is_published=True)

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
        activities = activities.filter(is_free=True)
    elif is_free_str == "paid":
        activities = activities.filter(is_free=False)


    search_query = request.GET.get("search","").strip()
    if search_query:
        activities = activities.filter(
            Q(name__icontains=search_query) |
            Q(location__name__icontains=search_query) 
        )

    activities = activities.order_by('start_date')

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


@login_required
@role_required(allowed_roles=['organizer','admin'])
def create_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit = False)
            activity.organizer = request.user
            activity.save()
            messages.success(request,'Etkinlik oluşturuldu.')
            return redirect(reverse_lazy('event:activity_detail', kwargs={'slug': activity.slug}))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    display_field_name = form.fields[field].label if field in form.fields else field
                    messages.error(request, f"{display_field_name}: {error}")
            for error in form.non_field_errors():
                messages.error(request, f"Hata: {error}")
    else:
        form = ActivityForm() 

    return render(request, 'organizer/create_activity.html', {'form': form})


@login_required
@role_required(allowed_roles=['organizer','admin'])
def my_activities(request):
    activities = Activity.objects.filter(organizer = request.user).order_by('-start_date')
    paginator = Paginator(activities, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'activities' : page_obj,
        'page_obj' : page_obj,
    }
    return render(request, 'organizer/my_activities.html', context)


@login_required
@role_required(allowed_roles=['organizer','admin'])
def edit_activity(request, slug):
    activity = get_object_or_404(Activity, slug=slug)

    if request.user != activity.organizer and request.user.role != 'admin':
        messages.error(request,"Etkinlik düzenleme yetkiniz yok")
        return redirect(reverse_lazy('event:activity_detail',kwargs={'slug':slug}))

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, "Etkinlik Güncellendi.")
            return redirect(reverse_lazy('event:activity_detail',kwargs={'slug' : activity.slug}))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    display_field_name = form.fields[field].label if field in form.fields else field
                    messages.error(request,f"{display_field_name}:{error}")
            for error in form.non_field_errors():
                messages.error(request,f"Hata : {error}")

    else:
        form = ActivityForm(instance = activity)

    return render(request, 'organizer/create_activity.html',{'form': form , 'activity': activity})

@csrf_exempt
@login_required
@role_required(allowed_roles=['organizer','admin'])
def delete_activity(request, slug):
    activity = get_object_or_404(Activity, slug=slug)

    if request.user != activity.organizer and request.user.role != 'admin':
        messages.error(request,"Etkinlik silme yetkiniz yok")
        return redirect(reverse_lazy('event:activity_detail',kwargs={'slug':slug}))
        
    if request.method == 'POST':
        print("POST geldi, silme işlemi başlıyor.")
        activity.delete()
        messages.success(request,"etkilik başarıyla silindi")
        print("Etkinlik silindi:", activity.slug)
        return redirect(reverse_lazy('event:my_activities'))

    return render(request,'organizer/delete_activity.html',{'activity':activity})

@login_required
def add_favorite(request, activity_id):
    activity = get_object_or_404(Activity , id = activity_id)
    favorite , created= Favorite.objects.get_or_create( user= request.user, activity = activity)

    if not created:
        favorite.delete()

    return redirect(request.META.get('HTTP_REFERER', 'event:home'))

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('activity')
    activities = [fav.activity for fav in favorites]
    return render(request, 'event/favorites_list.html', {'activities': activities})







    





