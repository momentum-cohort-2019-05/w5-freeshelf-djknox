from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/favorite/', views.favorite_book, name='favorite-book'),
    path('book/<int:pk>/comment/', views.comment_on_book, name='comment-book'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('favorites/', views.UserFavoritesListView.as_view(), name='favorites'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user-profile'),
    path('suggest/', views.suggest_book, name='suggest-book'),
    path('suggestions/', views.list_suggested_books, name='suggestions'),
    path('suggestions/<int:pk>/accept/', views.accept_suggested_book, name='accept-suggested-book'),
    path('suggestions/<int:pk>/decline/', views.decline_suggested_book, name='decline-suggested-book'),
]