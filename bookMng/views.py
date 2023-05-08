from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from .models import MainMenu
from .models import FavoriteList
from .forms import BookForm
from django.http import HttpResponseRedirect
from .models import Book
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Rating
from django.db.models import Avg


def index(request):
    return render(request, 'bookMng/index.html')


def displaybooks(request):
    favoriteBooks = None
    books = Book.objects.annotate(avg_rating=Avg('rating__value'))

    if request.user.is_authenticated:

        if FavoriteList.objects.filter(username=request.user).first():
            favorites_list = FavoriteList.objects.get(username=request.user)
            favoriteBooks = Book.objects.filter(favoriteLists=favorites_list)
            for book in favoriteBooks:
                book.pic_path = book.picture.url[14:]

    for book in books:
        book.pic_path = book.picture.url[14:]

        sorted_books = sorted(books, key=lambda book: book.name.lower())
        print('books:', books)



    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'books': books,
                      'favoriteBooks': favoriteBooks,
                      'sorted_books': sorted_books,
                  }
                  )

def remove_from_favorites(request,book_id):
    book = Book.objects.get(id=book_id)
    flist = FavoriteList(username=request.user)
    book.favoriteLists.remove(flist)
    favoriteBooks = None
    books = Book.objects.all()

    if FavoriteList.objects.filter(username=request.user).first():
        favorites_list = FavoriteList.objects.get(username=request.user)
        favoriteBooks = Book.objects.filter(favoriteLists=favorites_list)
        for book in favoriteBooks:
            book.pic_path = book.picture.url[14:]

    for book in books:
        book.pic_path = book.picture.url[14:]


    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'books': books,
                      'favoriteBooks': favoriteBooks,
                      'submitted': True
                  }
                  )


def add_to_favorites(request,book_id):
    book = Book.objects.get(id=book_id)
    if FavoriteList.objects.filter(username=request.user).first():
        flist = FavoriteList.objects.get(username=request.user)
    else:
        flist = FavoriteList(username=request.user)
        flist.save()
    book.favoriteLists.add(flist)
    books = Book.objects.all()

    for book in books:
        book.pic_path = book.picture.url[14:]

    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'books': books,
                      'submitted': True
                  }
                  )
def home(request):
    return render(request, 'bookMng/home.html')

def favoritesList(request):

    if FavoriteList.objects.filter(username=request.user).first():
        favorites_list = FavoriteList.objects.get(username=request.user)
        books = Book.objects.filter(favoriteLists=favorites_list)
        sorted_books = sorted(books, key=lambda book: book.name.lower()) if books else []
        for book in books:
            book.pic_path = book.picture.url[14:]

    else:
        books = None
        sorted_books = []

    return render(request,
                  'bookMng/favorite_list.html',
                  {
                      'books': books,
                      'sorted_books': sorted_books

                  }
                  )

def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'submitted': submitted,
                  }
                  )


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    average_rating = Rating.objects.filter(book=book).aggregate(Avg('value'))['value__avg']
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(book=book, user=request.user).first()

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'book': book,
                      'average_rating': average_rating,
                      'user_rating': user_rating

                  }

                  )


def mybooks(request):
    books = Book.objects.filter(username=request.user)
    sorted_books = sorted(books, key=lambda book: book.name.lower()) if books else []
    if len(books) == 0:
        books = None
    else:
        for book in books:
            book.pic_path = book.picture.url[14:]

    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'books': books,
                      'sorted_books': sorted_books
                  }
                  )


def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html')


def search(request):
    query = request.GET.get('q')
    books = Book.objects.filter(
        Q(name__icontains=query)
    )
    if len(books) == 0:
        books = None
    else:
        for book in books:
            book.pic_path = book.picture.url[14:]
    return render(request, 'bookMng/search.html', {'books': books})


def submit_rating(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(id=book_id)
        rating_value = request.POST.get('value')
        user_rating = Rating.objects.filter(book=book, user=request.user).first()
        if user_rating:
            user_rating.value = rating_value
            user_rating.save()
        else:
            Rating.objects.create(book=book, user=request.user, value=rating_value)
    return redirect('book_detail', book_id=book_id)
