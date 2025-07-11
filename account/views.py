from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from django.contrib import messages




def login_request(request):
    if request.user.is_authenticated:
       return redirect("event:home") 
    

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request,user)
            return redirect("event:home") 
        else:
            messages.error(request, "Kullanıcı adı veya parola hatalı.")
            return render(request,"account/login.html",{
            })
        
    return render(request,"account/login.html")    


def register_request(request):
    if request.user.is_authenticated:
        return redirect("event:home") 
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username = username).exists():
                messages.error(request, "Kullanıcı adı kullanılıyor.")
                return render(request,"account/register.html",{
                     "username":username,
                     "email":email,
                     "firstname":firstname,
                     "lastname":lastname,
                })
            else:
                if User.objects.filter(email = email).exists():
                    messages.error(request, "Email kullanılıyor.")
                    return render(request,"account/register.html",{
                     "username":username,
                     "email":email,
                     "firstname":firstname,
                     "lastname":lastname,
                    })
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=firstname,
                        last_name=lastname,
                        password=password
                    )
                    user.save()
                    return redirect("account:login")
                


        else:
            messages.error(request, "Parola Eşleşmiyor.")
            return render(request,"account/register.html",{

                "username" : username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname
            })


    return render (request,"account/register.html")    


def logout_request(request):
    logout(request)
    return redirect("event:home") 