from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library, Book, Author
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required



def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = "library"

# Registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

# Role checks
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == "Member"

# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

# Add Book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author")
        publication_year = request.POST.get("publication_year") or None
        author = Author.objects.get(id=author_id)
        Book.objects.create(title=title, author=author, publication_year=publication_year)
        return redirect("list_books")
    authors = Author.objects.all()
    return render(request, "relationship_app/add_book.html", {"authors": authors})

# Edit Book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title")
        author_id = request.POST.get("author")
        book.author = Author.objects.get(id=author_id)
        book.publication_year = request.POST.get("publication_year") or None
        book.save()
        return redirect("list_books")
    authors = Author.objects.all()
    return render(request, "relationship_app/edit_book.html", {"book": book, "authors": authors})

# Delete Book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "relationship_app/delete_book.html", {"book": book})
