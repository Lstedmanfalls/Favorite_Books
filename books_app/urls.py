from django.urls import path
from . import views

urlpatterns = [
    path('book', views.book), #GET request to display all objects' info starting at a different root
    # path('book/new_book', views.add_book), #GET request to display form to create an object
    # path('book/create_book', views.create_book), #POST request to create an object
    # path('book/<int:book_id>', views.view_book), #GET request to display a specific object's info
    # path('book/<int:book_id>/edit', views.edit_book), #GET request to display form to update a specific object
    # path('book/<int:book_id>/update', views.update_book), #POST request to update a specific object
    # path('book/<int:book_id>/destroy', views.delete_book), #POST request to delete a specific object
]