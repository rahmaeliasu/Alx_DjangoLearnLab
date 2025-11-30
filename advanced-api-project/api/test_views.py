from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Unit tests for Book API endpoints.
    Covers:
    - CRUD operations
    - Authentication/permission behaviors
    - Filtering, searching, and ordering
    """

    def setUp(self):
        # Create user for authenticated actions
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        # Create Author
        self.author = Author.objects.create(name="Author 1")

        # Existing books
        self.book1 = Book.objects.create(
            title="Alpha Book",
            publication_year=2020,
            author=self.author,
        )
        self.book2 = Book.objects.create(
            title="Beta Book",
            publication_year=2023,
            author=self.author,
        )

        # URLs
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = reverse("book-detail", args=[self.book1.id])
        self.update_url = reverse("book-update", args=[self.book1.id])
        self.delete_url = reverse("book-delete", args=[self.book1.id])

    # -----------------------------------------------------

    def test_list_books(self):
        """Unauthenticated users should be able to view the list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # -----------------------------------------------------

    def test_create_book_authenticated(self):
        """Only authenticated users can create books."""
        self.client.login(username="testuser", password="testpass123")

        data = {
            "title": "Created Book",
            "publication_year": 2024,
            "author": self.author.id,
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create books."""
        data = {
            "title": "New Book",
            "publication_year": 2024,
            "author": self.author.id,
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------------------------------

    def test_update_book_authenticated(self):
        """Authenticated users can update a book."""
        self.client.login(username="testuser", password="testpass123")

        data = {
            "title": "Updated Book",
            "publication_year": 2021,
            "author": self.author.id,
        }

        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")

    def test_update_book_unauthenticated(self):
        """Unauthenticated users cannot update."""
        data = {
            "title": "Unauthorized Update",
            "publication_year": 2021,
            "author": self.author.id,
        }

        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------------------------------

    def test_delete_book_authenticated(self):
        """Authenticated users can delete a book."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        """Unauthenticated delete should fail."""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------------------------------

    def test_filter_books(self):
        """Filter by title using ?title=Alpha Book."""
        response = self.client.get(self.list_url + "?title=Alpha Book")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Alpha Book")

    def test_search_books(self):
        """Search by text using ?search=Alpha."""
        response = self.client.get(self.list_url + "?search=Alpha")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        """Order books by title using ?ordering=title."""
        response = self.client.get(self.list_url + "?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Alpha Book")  # alphabetically first
