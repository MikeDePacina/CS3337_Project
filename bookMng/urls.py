from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('displaybooks/add/<int:book_id>', views.add_to_favorites, name='addToFavorites'),
    path('displaybooks/remove/<int:book_id>', views.remove_from_favorites, name='removeFromFavorites'),
    path('favorites_list', views.favoritesList,name='favoritesList'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('search', views.search, name='search'),
    path('submit_rating/<int:book_id>/', views.submit_rating, name='submit_rating'),

]
