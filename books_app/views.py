from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Book, User
from django.db.models import Sum
import bcrypt

def get_books(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")

    context = {
    "users": User.objects.all(),
    "user": User.objects.get(id=request.session["user_id"]),
    "books": Book.objects.all(),
    }
    return render(request, "books.html", context)

def create_book(request):
    if request.method != "POST":
        return redirect("/book")
    
    errors = Book.objects.create_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/book")

    uploader = User.objects.get(id = request.session["user_id"]) 
    create = Book.objects.create(title = request.POST["title"], description = request.POST["description"], genre = request.POST["genre"], uploaded_by = uploader)
    book = Book.objects.get(id = create.id)
    book.favorited_by.add(uploader)
    return redirect("/book")

def unfavorite_on_homepage(request, book_id):
    if request.method != "POST":
        return redirect("/book")
    
    user = User.objects.get(id = request.session["user_id"])
    book = Book.objects.get(id = book_id)
    user.books_favorited.remove(book)
    return redirect("/book")

def favorite_on_homepage(request, book_id):
    if request.method != "POST":
        return redirect("/book")
    
    user = User.objects.get(id = request.session["user_id"])
    book = Book.objects.get(id = book_id)
    user.books_favorited.add(book)
    return redirect("/book")

def get_book(request, book_id):
    book = Book.objects.get(id = book_id)
    user = User.objects.get(id = request.session["user_id"])
    admin = User.objects.get(id = 1)
    context = {
        "user": user,
        "book": book,
        "favorited_by": book.favorited_by.all(),
        "user_who_uploaded":book.uploaded_by,
        "admin": admin,
    }
    return render(request, "book_page.html", context)

def unfavorite_on_bookpage(request, book_id):
    if request.method != "POST":
        return redirect(f"/book/{book_id}")
    
    user = User.objects.get(id = request.session["user_id"])
    book = Book.objects.get(id = book_id)
    user.books_favorited.remove(book)
    return redirect(f"/book/{book_id}")

def favorite_on_bookpage(request, book_id):
    if request.method != "POST":
        return redirect(f"/book/{book_id}")

    user = User.objects.get(id = request.session["user_id"])
    book = Book.objects.get(id = book_id)
    user.books_favorited.add(book)
    return redirect(f"/book/{book_id}")

def update_book(request, book_id):
    if request.method != "POST":
        return redirect(f"/book/{book_id}")

    book = Book.objects.get(id = book_id)
    errors = Book.objects.update_validator(request.POST)
    if request.POST['title'] == book.title and request.POST['genre'] == book.genre and request.POST['description'] == book.description:
        messages.success(request, "No changes made")
        return redirect(f"/book/{book_id}")
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/book/{book_id}")

    book.title = request.POST["title"]
    book.genre = request.POST["genre"]
    book.description = request.POST["description"]
    book.save()
    messages.success(request, "Book updated")
    return redirect(f"/book/{book_id}")

def delete_book(request, book_id):
    if request.method != "POST":
        return redirect(f"/book/{book_id}")

    book = Book.objects.get(id = book_id)
    book.delete()
    return redirect("/book")

def user_page(request, user_id):
    user = User.objects.get(id=request.session["user_id"])
    view_user = User.objects.get(id = user_id)
    admin = User.objects.get(id = 1)
    uploaded_books = view_user.books_uploaded.all()
    book_count = uploaded_books.count()
    favorited_books = view_user.books_favorited.all()
    favorite_count= favorited_books.count()
    context = {
        "user": user,
        "view_user": view_user,
        "favorited_books": favorited_books,
        "uploaded_books":uploaded_books,
        "book_count": book_count,
        "favorite_count":favorite_count,
        "admin": admin,
    }
    return render(request, "user_page.html", context)

def edit_info(request, user_id):
    if request.method != "POST":
        return redirect(f"/book/user/{user_id}")
    
    view_user = User.objects.get(id = user_id)
    errors = Book.objects.edit_info_validator(request.POST, request.session)    
    if request.POST['username'] == view_user.username and request.POST['bio'] == view_user.bio:
        messages.success(request, "No changes made")
        return redirect(f"/book/user/{user_id}")
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/book/user/{user_id}")

    view_user.bio = request.POST["bio"]
    view_user.username = request.POST["username"]
    view_user.save()
    messages.success(request, "Info updated")
    return redirect(f"/book/user/{user_id}")

def change_password(request, user_id):
    if request.method != "POST":
        return redirect(f"/book/user/{user_id}")
    errors = Book.objects.change_password_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/book/user/{user_id}")

    view_user = User.objects.get(id = user_id)
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    view_user.password = pw_hash
    view_user.save()
    messages.success(request, "Password updated")
    return redirect(f"/book/user/{user_id}")