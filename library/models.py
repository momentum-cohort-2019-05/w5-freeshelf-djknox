from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Author(models.Model):
    """Model representing an author."""
    name = models.CharField(max_length=200, help_text='Enter the name of the author')

    # def get_absolute_url(self):
    #     """Returns the url to access a particular author instance."""
    #     return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Author object."""
        return self.name


class Category(models.Model):
    """Model representing a book category."""
    name = models.CharField(max_length=200, help_text='Enter a book category (e.g. Python)')

    class Meta:
            verbose_name_plural = "categories"
    
    def __str__(self):
        """String for representing the Category object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this category."""
        return reverse('category-detail', args=[str(self.id)])


class Book(models.Model):
    """Model representing a book."""
    title = models.CharField(max_length=200, help_text='Enter the title of the book')
    url = models.URLField(max_length=200, unique=True, help_text='Enter the URL of the book')
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    image = models.ImageField(null=True, blank=True, upload_to='books')
    created_date = models.DateTimeField(auto_now_add=True)

    # a book can only have one author, but authors can have multiple books
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    # a book can have many categories, and a category can have many books
    categories = models.ManyToManyField(Category, help_text='Select categories for this book')
    favorites = models.ManyToManyField(User, through='Favorite')

    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        """String for representing the Book object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def get_num_favorites(self):
        """Returns the number of times the book has been favorited by a user."""
        return self.favorites.count()


class Favorite(models.Model):
    """A User can favorite many Books and a Book can be favorited by many Users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        """String for representing the Favorite object."""
        return f"{self.user.username} - {self.book.title}"


class Comment(models.Model):
    """A Comment is made on one Book and is made by one User"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField(help_text='Write your comment here.')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date',]

    def __str__(self):
        """String for representing the Comment object."""
        return f"{self.user.username} - {self.text}"


class SuggestedBook(models.Model):
    """Model representing a suggested book."""
    title = models.CharField(max_length=200, help_text='Enter the title of the book')
    author = models.CharField(max_length=200, help_text='Enter the author of the book')
    url = models.URLField(max_length=200, unique=True, help_text='Enter the URL of the book')
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    created_date = models.DateTimeField(auto_now_add=True)

    # a SuggestedBook is suggested by a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the SuggestedBook object."""
        return f"{self.user.username} suggested: \"{self.title}\" by {self.author}"