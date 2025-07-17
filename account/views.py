from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from django.contrib.auth.models import Group 
from django.views.decorators.csrf import csrf_exempt


def register_request(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.role = 'attendee'        
            user.is_active = True        
            user.save()                  

            attendee_group, created = Group.objects.get_or_create(name='Attendees')
            user.groups.add(attendee_group) 

            login(request, user)
            messages.success(request, "Kayıt başarılı. Hoş geldiniz!")
            return redirect("event:home") 

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    display_field_name = form.fields[field].label if field in form.fields else field
                    messages.error(request, f"{display_field_name}: {error}")
            for error in form.non_field_errors():
                messages.error(request, f"Genel Hata: {error}")

            return render(request, "account/register.html", {"form": form})
            
    form = CustomUserCreationForm()
    return render(request, "account/register.html", {"form": form})

@csrf_exempt
def login_request(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) 
            if user is not None:
                login(request, user)
                return redirect("event:home")  
            else:
                messages.error(request, "Geçersiz kullanıcı adı veya parola.")
        else:
            messages.error(request, "Lütfen formu doğru doldurun.") 
    
   
    form = CustomAuthenticationForm()
    return render(request, "account/login.html", {"form": form})


def logout_request(request):
    logout(request)
    return redirect("event:home")

def home(request):
    return render(request, "event/activity_list.html", {})