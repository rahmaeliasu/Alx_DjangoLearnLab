# Update Operation

**Command**
```python
from bookshelf.models import Book

# Retrieve and update the title of the book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book

# Expected Output
# <Book: Nineteen Eighty-Four by George Orwell>
