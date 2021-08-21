from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Book, User
from django.db.models import Sum

def book(request): #GET REQUEST
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        context = {
        "all_the_users": User.objects.all(),
        "this_user": User.objects.get(id=request.session["user_id"]),
        "all_the_books": Book.objects.all(),
    }
    return render(request, "books.html", context)

def create_book(request): #POST REQUEST
    errors = Book.objects.create_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/book")
    elif request.method != "POST":
        return redirect("/book")
    elif request.method == "POST":
        uploader = User.objects.get(id = request.session["user_id"]) 
        create = Book.objects.create(title = request.POST["title"], description = request.POST["description"], uploaded_by = uploader)
        this_book = Book.objects.get(id = create.id)
        this_book.favorited_by.add(uploader)
    return redirect("/book")

def unfavorite_homepage(request, book_id): #POST Request
    this_user = User.objects.get(id = request.session["user_id"])
    this_book = Book.objects.get(id = book_id)
    if request.method != "POST":
        return redirect("/book")
    if request.method == "POST":
        this_user.books_favorited.remove(this_book)
    return redirect("/book")

def favorite_homepage(request, book_id): #POST Request
    this_user = User.objects.get(id = request.session["user_id"])
    this_book = Book.objects.get(id = book_id)
    if request.method != "POST":
        return redirect("/book")
    if request.method == "POST":
        this_user.books_favorited.add(this_book)
        return redirect("/book")

def view_book(request, book_id): #GET REQUEST
    this_book = Book.objects.get(id = book_id)
    this_user = User.objects.get(id = request.session["user_id"])
    context = {
        "this_user": this_user,
        "a_book": this_book,
        "favorited_by": this_book.favorited_by.all(),
        "user_who_uploaded":this_book.uploaded_by,
    }
    return render(request, "view_book.html", context)

def unfavorite_bookpage(request, book_id): #POST Request
    this_user = User.objects.get(id = request.session["user_id"])
    this_book = Book.objects.get(id = book_id)
    if request.method != "POST":
        return redirect(f"/book/{book_id}")
    if request.method == "POST":
        this_user.books_favorited.remove(this_book)
    return redirect(f"/book/{book_id}")

def favorite_bookpage(request, book_id): #POST Request
    this_user = User.objects.get(id = request.session["user_id"])
    this_book = Book.objects.get(id = book_id)
    if request.method != "POST":
        return redirect(f"/book/{book_id}")
    if request.method == "POST":
        this_user.books_favorited.add(this_book)
    return redirect(f"/book/{book_id}")

def update_book(request, book_id): #POST REQUEST
    errors = Book.objects.update_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/book/{book_id}")
    elif request.method != "POST":
        return redirect(f"/book/{book_id}")
    elif request.method == "POST":
        a_book = Book.objects.get(id = book_id)
        a_book.title = request.POST["title"]
        a_book.description = request.POST["description"]
        a_book.save()
        messages.success(request, "Book updated")
    return redirect(f"/book/{book_id}")

def destroy_book(request, book_id): #POST Request
    if request.method != "POST":
        return redirect(f"/book/{book_id}")
    if request.method == "POST":
        a_book = Book.objects.get(id = book_id)
        a_book.delete()
    return redirect("/book")

def user_page(request, user_id): #GET REQUEST
    this_user= User.objects.get(id=request.session["user_id"])
    a_user = User.objects.get(id = user_id)
    uploaded_books = a_user.books_uploaded.all()
    book_count = uploaded_books.count()
    context = {
        "this_user":this_user,
        "a_user": a_user,
        "favorited_books": a_user.books_favorited.all(),
        "uploaded_books":uploaded_books,
        "book_count": book_count,
    }
    return render(request, "user_page.html", context)