from django.contrib import admin
from library.models import Author, Book, Category

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)