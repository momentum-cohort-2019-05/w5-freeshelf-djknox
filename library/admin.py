from django.contrib import admin
from library.models import Author, Book, Category, Favorite, Comment

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(Comment)