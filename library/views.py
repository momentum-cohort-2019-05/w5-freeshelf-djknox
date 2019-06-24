from django.shortcuts import render
from library.models import Book, Author
from django.views import generic


def index(request):
    """View function for home page of site."""

    # Generate counts of books and authors
    num_books = Book.objects.all().count()
    num_authors = Author.objects.count()

    # get three latest books
    latest_books = Book.objects.order_by('-created_date')[:3]
    
    context = {
        'latest_books': latest_books,
        'num_books': num_books,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context)


class BookListView(generic.ListView):
    model = Book


class BookDetailView(generic.DetailView):
    model = Book