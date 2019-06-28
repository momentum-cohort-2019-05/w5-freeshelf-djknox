from django.shortcuts import render
from library.models import Book, Author, Category, Favorite, Comment, User, SuggestedBook
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from library.forms import BookCommentForm, BookSuggestForm


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

    def get_queryset(self):
        # GET parameter can order by created_date or title
        order_by = self.request.GET.get('order_by')
        if order_by in ['created_date', '-created_date', 'title', '-title']:
            return Book.objects.order_by(order_by)
        else:
            return Book.objects.all()


class BookDetailView(generic.DetailView):
    model = Book


class CategoryListView(generic.ListView):
    model = Category


class CategoryDetailView(generic.DetailView):
    model = Category


class UserFavoritesListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books that have been favorited by current user."""
    model = Favorite
    template_name ='library/user_favorites_list.html'
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


def favorite_book(request, pk):
    """View function for favoriting a Book by a User."""
    book = get_object_or_404(Book, pk=pk)

    # if the request is a GET (the user requests the /book/<book>/favorite url)
    # book.favorites.add(request.user)
    if request.method == 'GET':
        if request.user in book.favorites.all():
            book.favorites.remove(request.user)
        else:
            book.favorites.add(request.user)

    # redirect to a new URL:
    return HttpResponseRedirect(request.GET.get("next"))


def comment_on_book(request, pk):
    """View function for commenting on a Book by a User."""
    book = get_object_or_404(Book, pk=pk)

    # if the request is a POST (the user submits the form to /book/<book>/comment)
    if request.method == 'POST':
        form = BookCommentForm(request.POST)

        if form.is_valid():
            comment = Comment(book=book, user=request.user, text=form.cleaned_data['text'])
            comment.save()

        # redirect to a new URL:
        return HttpResponseRedirect(reverse_lazy('book-detail', kwargs = {'pk': pk}))

    # If the request is a GET then show the form
    else:
        form = BookCommentForm()

        context = {
            'form': form,
            'book': book,
        }

        return render(request, 'library/book_comment.html', context)


class UserDetailView(generic.DetailView):
    model = User
    template_name ='library/user_detail.html'


def suggest_book(request):
    """View function for a User to suggest a Book."""

    # if the request is a POST (the user submits the form to /suggest/)
    if request.method == 'POST':
        form = BookSuggestForm(request.POST)

        if form.is_valid():
            suggested_book = SuggestedBook(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                url=form.cleaned_data['url'],
                description=form.cleaned_data['description'],
            )
            suggested_book.user = request.user
            suggested_book.save()

        # redirect to a new URL:
        return HttpResponseRedirect(reverse_lazy('suggest-book'))
    # If the request is a GET then show the form
    else:
        form = BookSuggestForm()
        return render(request, 'library/book_suggest.html', {'form': form})


class SuggestedBookListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing of all books that have been suggested by all users."""
    model = SuggestedBook
    template_name ='library/suggested_books.html'


def accept_suggested_book(request, pk):
    """View function for accepting a SuggestedBook and creating a Book."""
    suggested_book = get_object_or_404(SuggestedBook, pk=pk)

    # if the request is a GET (the user requests the /suggestions/<book>/accept url)
    # create a Book from the SuggestedBook object and remove SuggestedBook
    if request.method == 'GET':
        # check to see if author already exists
        author = Author.objects.filter(name=suggested_book.author).first()
        if not author:
            author = Author(name = suggested_book.author)
            author.save()

        Book(
            title = suggested_book.title,
            author = author,
            url = suggested_book.url,
            description = suggested_book.description
        ).save()

        suggested_book.delete()

    # redirect to a new URL:
    return HttpResponseRedirect(request.GET.get("next"))


def decline_suggested_book(request, pk):
    """View function for declining a SuggestedBook."""
    suggested_book = get_object_or_404(SuggestedBook, pk=pk)

    # if the request is a GET (the user requests the /suggestions/<book>/decline url)
    # create a Book from the SuggestedBook object and remove SuggestedBook
    if request.method == 'GET':
        suggested_book.delete()

    # redirect to a new URL:
    return HttpResponseRedirect(request.GET.get("next"))
