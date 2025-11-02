# Delete Operation

**Command**
```python
from bookshelf.models import Book

# Retrieve and delete the book instance
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by retrieving all books
Book.objects.all()

# Expected Output
# (1, {'bookshelf.Book': 1})
# <QuerySet []>
