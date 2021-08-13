from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        existing_email = User.objects.filter(email = postData["email"])
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters"
        elif postData["password"] != postData["password_confirm"]:
            errors["password_confirm"] = "Passwords do not match"
        if not EMAIL_REGEX.match(postData["email"]):           
            errors["email"] = "Email address not valid"
        elif len(existing_email) > 0:
            errors["duplicate_email"] = "Email already registered"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData["email"])[0]
        if not bcrypt.checkpw(postData["password"].encode(), user.password.encode()):
            errors['invalid_password'] = "That password is incorrect"
            print('password is incorrect')
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #books_uploaded
    #books_favorited
    def __repr__(self):
        uploaded_books = ""
        favorited_books = ""
        for book in self.books_uploaded.all():
            uploaded_books += book.title + ","
        for book in self.books_favorited.all():
            favorited_books += book.title + ","
        return f"Users: Id = {self.id}, First Name = {self.first_name}, Last Name = {self.last_name}, Email = {self.email}, Password = {self.password}, Uploaded Books = {uploaded_books}, Favorited Books = {favorited_books}"