from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Article

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
