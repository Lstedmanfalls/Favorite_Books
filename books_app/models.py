from django.db import models
from login_registration_app.models import User

class BookManager(models.Manager):
    
    def create_validator(self, postData):
        existing_books = Book.objects.filter(title = postData['title'])
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Title is required and must be at least 1 character long"
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

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=255, default="")
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