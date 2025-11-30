from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# ----------------------------------------
# List all books
# ----------------------------------------
class BookListView(generics.ListAPIView):
    """
    GET /books/
    Returns a list of all books.
    Read-only access, available to anyone.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  ## read-only for unauthenticated users


# ----------------------------------------
# Retrieve a single book by ID
# ----------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<int:pk>/
    Returns the details of a single book.
    Read-only access, available to anyone.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ----------------------------------------
# Create a new book
# ----------------------------------------
class BookCreateView(generics.CreateAPIView):
    """
    POST /books/create/
    Allows authenticated users to add a new book.
    Includes validation from BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # must be logged in


# ----------------------------------------
# Update an existing book
# ----------------------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT /books/<int:pk>/update/
    Allows authenticated users to update book details.
    Includes validation from BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ----------------------------------------
# Delete a book
# ----------------------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<int:pk>/delete/
    Allows authenticated users to delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
