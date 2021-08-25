from django.db import models
from login_registration_app.models import User

class BookManager(models.Manager):
    
    def create_validator(self, postData):
        existing_books = Book.objects.filter(title = postData['title'])
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Title is required and must be at least 1 character long"
        elif len(existing_books) > 0:
            errors['duplicate_book'] = "Book already exists. Please choose another one."
        if len(postData['genre']) < 5:
            errors['genre'] = "Genre must be at least 5 characters long"
        if len(postData['description']) < 5:
            errors['description'] = "Description must be at least 5 characters long"
        elif len(existing_books) > 0:
            errors['duplicate'] = "That book already exists"
        return errors

    def update_validator(self, postData):
        existing_books = Book.objects.filter(title = postData['title'])
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Title is required"
        if len(postData['genre']) < 3:
            errors['genre'] = "Genre must be at least 3 characters long"
        if len(postData['description']) < 5:
            errors['description'] = "Description must be at least 5 characters long"
        return errors
    
    def edit_info_validator(self, postData):
        existing_username = User.objects.filter(username = postData["username"])
        errors = {}
        if len (postData['bio']) > 0 and len (postData['bio']) < 10:
            errors["bio"] = "Bio may be blank or at least 10 characters."
        if len(postData['username']) < 1:
            errors["username"] = "Username is required."
        elif len(existing_username) > 0:
            errors['duplicate_username'] = "Username already exists. Please choose another one."
        return errors
    
    def change_password_validator(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters."
        elif postData["password"] != postData["password_confirm"]:
            errors["password_confirm"] = "Passwords do not match."
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name = "books_uploaded", on_delete = models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name = "books_favorited")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    def __repr__(self):
        user_uploaded = ""
        users_favorited = ""
        for user in self.uploaded_by.all():
            user_uploaded += user.first_name + ","
        for user in self.favorited_by.all():
            users_favorited += user.first_name + ","
        return f"Books: id = {self.id}, description = {self.description}, uploaded by = {user_uploaded}, favorited by = {users_favorited}"