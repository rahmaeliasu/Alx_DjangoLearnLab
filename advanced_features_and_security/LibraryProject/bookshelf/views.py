from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book, Article
from .forms import ExampleForm, BookForm, SearchForm

def example_view(request):
    form = ExampleForm()
    return render(request, "example.html", {"form": form})


def book_list(request):
    form = SearchForm(request.GET)
    qs = Book.objects.all()
    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            # Use ORM lookups (parameterized automatically)
            qs = qs.filter(title__icontains=q)
    return render(request, "bookshelf/book_list.html", {"books": qs, "form": form})


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/book_form.html", {"form": form})


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/book_form.html", {"form": form})


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "bookshelf/book_confirm_delete.html", {"book": book})


# VIEW
@permission_required("bookshelf.can_view", raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, "articles/list.html", {"articles": articles})


# CREATE
@permission_required("bookshelf.can_create", raise_exception=True)
def article_create(request):
    if request.method == "POST":
        Article.objects.create(
            title=request.POST["title"],
            content=request.POST["content"],
            author=request.user
        )
        return redirect("article_list")
    return render(request, "articles/create.html")


# EDIT
@permission_required("bookshelf.can_edit", raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.title = request.POST["title"]
        article.content = request.POST["content"]
        article.save()
        return redirect("article_list")
    return render(request, "articles/edit.html", {"article": article})


# DELETE
@permission_required("bookshelf.can_delete", raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect("article_list")
