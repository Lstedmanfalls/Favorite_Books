from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, UserManager
import bcrypt

def index(request):
    context = {
    "users": User.objects.all(),
    }
    return render(request, "index.html", context)

def register(request):
    if request.method != "POST":
        return redirect("/")
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user_id = User.objects.create(first_name = request.POST["first_name"], last_name = request.POST["last_name"], username = request.POST["username"], email = request.POST['email'], password=pw_hash)
    request.session['user_id'] = user_id.id
    return redirect("/book")

def login(request):
    if request.method != "POST":
        return redirect("/")
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    
    user = User.objects.filter(email=request.POST["email"])
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session["user_id"] = logged_user.id
            return redirect("/book")
        return redirect("/")
    return redirect("/")

def logout(request):
    if request.method != "POST":
        return redirect("/")
    request.session.flush()
    return redirect("/")