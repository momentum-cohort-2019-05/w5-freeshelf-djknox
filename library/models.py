from django.db import models
from django.urls import reverse
from django.utils import timezone

class Author(models.Model):
    """Model representing an author."""
    name = models.CharField(max_length=200, help_text='Enter the name of the author')

    # def get_absolute_url(self):
    #     """Returns the url to access a particular author instance."""
    #     return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Author object."""
        return self.name


class Book(models.Model):
    """Model representing a book."""
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200, unique=True, help_text='Enter the URL of the book')
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    image = models.ImageField(null=True, upload_to='books')
    created_date = models.DateTimeField(auto_now_add=True)

    # a book can only have one author, but authors can have multiple books
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        """String for representing the Book object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])