# 📝 Testing Documentation – advanced-api-project

## 1. Testing Strategy

The API endpoints for the `Book` model are thoroughly tested using **Django REST Framework’s testing framework** (`APITestCase`), which is built on Python’s `unittest` module.

Key points of the testing strategy:

- **CRUD Operations:** All Create, Read, Update, Delete endpoints for `Book` are tested to ensure correct functionality and response codes.
- **Authentication & Permissions:** Tests verify that only authenticated users can create, update, or delete books, while unauthenticated users have read-only access.
- **Filtering, Searching, Ordering:** Tests ensure the list endpoint supports query parameters for filtering by title, author, or publication year, searching by text, and ordering by fields like title or publication year.
- **Data Integrity:** Tests check that data is correctly saved, updated, and deleted in the database, and that foreign key relationships (Author → Book) are correctly maintained.
- **Isolated Testing Environment:** Tests use Django’s test database, ensuring no impact on development or production data.

---

## 2. Individual Test Cases

| Test Case | Description | Expected Outcome |
|-----------|------------|----------------|
| `test_list_books` | Retrieve all books (unauthenticated) | Returns 200 OK and correct number of books |
| `test_get_single_book` | Retrieve a specific book by ID | Returns 200 OK and correct book data |
| `test_create_book_authenticated` | Authenticated user creates a book | Returns 201 Created and book is saved |
| `test_create_book_unauthenticated` | Unauthenticated user tries to create a book | Returns 403 Forbidden |
| `test_update_book_authenticated` | Authenticated user updates a book | Returns 200 OK and changes are applied |
| `test_update_book_unauthenticated` | Unauthenticated user tries to update | Returns 403 Forbidden |
| `test_delete_book_authenticated` | Authenticated user deletes a book | Returns 204 No Content and book removed |
| `test_delete_book_unauthenticated` | Unauthenticated user tries to delete | Returns 403 Forbidden |
| `test_filter_books` | Filter books by title, author, or publication year | Returns 200 OK and correct filtered results |
| `test_search_books` | Search books by text query (title or author) | Returns 200 OK and matching results |
| `test_order_books` | Order books by a field (title, publication_year) | Returns 200 OK and correctly ordered list |

---

## 3. How to Run Tests

1. Ensure your **virtual environment is activated**.
2. Run the following command from the project root:

```bash
python manage.py test api
