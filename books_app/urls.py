from django.urls import path
from . import views

urlpatterns = [
    path('', views.book), #GET request to display all objects' info starting at a different root
    path('create_book', views.create_book), #POST request to create an object
    path('<int:book_id>/unfavorite_homepage', views.unfavorite_homepage),
    path('<int:book_id>/favorite_homepage', views.favorite_homepage),
    path('<int:book_id>', views.view_book), #GET request to display a specific object's info
    path('<int:book_id>/unfavorite_bookpage', views.unfavorite_bookpage),
    path('<int:book_id>/favorite_bookpage', views.favorite_bookpage),
    path('<int:book_id>/update_book', views.update_book), #POST request to update a specific object
    path('<int:book_id>/destroy_book', views.destroy_book), #POST request to delete a specific object
    path('user/<int:user_id>', views.user_page), #GET request to display a specific object's info
    path('user/<int:user_id>/edit_bio', views.edit_bio),
    path('user/<int:user_id>/change_password', views.change_password),
]