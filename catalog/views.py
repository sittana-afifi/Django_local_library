
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
import datetime
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, request
from django.urls import reverse
from catalog.forms import RenewBookForm , BorrowBookForm 
from django.contrib.auth.decorators import login_required, permission_required


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    #x = Book.objects.filter(author='author')

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


    

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

  

class BookDetailView(generic.DetailView):
    model = Book

class AuthorDetailView(generic.DetailView):
    model = Author
    
    
    def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
            context = super().get_context_data(**kwargs)
            # Add in a QuerySet of all the books
            #####
            #context['list'] = Book.objects.all().filter(author.id = Book.author_id)
            context['booksByAuthor'] = Book.objects.all().filter(author= context.get('author'))
            
            return context
 


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    #permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class BorrowedListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/borrowed_list.html'



@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author , Book

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '2020-11-06'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = ['author', 'summary', 'isbn', 'genre']
    
class BookUpdate(UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')




class BorrowBookListView(generic.ListView): 
    model = BookInstance
    template_name ='catalog/borrow_book_list.html'
    
    def get_queryset(self):
        books=BookInstance.objects.all().filter(status='a').distinct('book').order_by('pk')
        return books


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def borrow_book_librarian(request, pk):
    """View function for borrowing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)
  
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = BorrowBookForm(request.POST)

        # Check if the form is valid:
        
       
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            
            
            book_instance.due_back = form.cleaned_data['borrow_date']
            book_instance.borrower = form.cleaned_data['user']
            print(book_instance.id )
            #book_instance.book = form.cleaned_data['book']
            book_instance.status = 'o'
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrow_book_view') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_borrow_date = datetime.date.today() 
       # proposed_due_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = BorrowBookForm(initial={'borrow_date': proposed_borrow_date})
        #form = BorrowBookForm(initial={'due_back': proposed_due_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }
    
    return render(request, 'catalog/book_borrow_librarian.html', context)

