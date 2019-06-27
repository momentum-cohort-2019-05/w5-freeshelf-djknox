from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('favorites/', views.UserFavoritesListView.as_view(), name='favorites'),
    path('book/<int:pk>/favorite', views.favorite_book, name='favorite-book'),
    path('book/<int:pk>/comment', views.comment_on_book, name='comment-book'),
]