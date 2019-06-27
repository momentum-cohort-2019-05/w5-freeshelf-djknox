from django.shortcuts import render
from library.models import Book, Author, Category, Favorite, Comment, User
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from library.forms import BookCommentForm


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
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
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