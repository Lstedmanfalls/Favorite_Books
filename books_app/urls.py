from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_books),
    path('create_book', views.create_book),
    path('<int:book_id>/unfavorite_homepage', views.unfavorite_on_homepage),
    path('<int:book_id>/favorite_homepage', views.favorite_on_homepage),
    path('<int:book_id>', views.get_book),
    path('<int:book_id>/unfavorite_bookpage', views.unfavorite_on_bookpage),
    path('<int:book_id>/favorite_bookpage', views.favorite_on_bookpage),
    path('<int:book_id>/update_book', views.update_book),
    path('<int:book_id>/destroy_book', views.delete_book),
    path('user/<int:user_id>', views.user_page),
    path('user/<int:user_id>/edit_info', views.edit_info),
    path('user/<int:user_id>/change_password', views.change_password),
]