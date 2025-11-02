from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # columns shown in list view
    list_filter = ('author', 'publication_year')            # filter sidebar
    search_fields = ('title', 'author')                     # search box fields

admin.site.register(Book, BookAdmin)
