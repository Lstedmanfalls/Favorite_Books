from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Book, Favorite, User

def book(request): #GET REQUEST
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        context = {
        "this_user": User.get(id=request.session["user_id"]),
        "all_the_books": Book.objects.all(),
    }
    return render(request, "books.html", context)