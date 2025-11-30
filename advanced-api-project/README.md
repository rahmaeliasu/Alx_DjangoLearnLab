## Book API Endpoints

- GET /api/books/ → List all books (public)
- GET /api/books/<id>/ → Retrieve a single book (public)
- POST /api/books/create/ → Create book (authenticated)
- PUT /api/books/<id>/update/ → Update book (authenticated)
- DELETE /api/books/<id>/delete/ → Delete book (authenticated)

All create/update operations validate publication_year to ensure it’s not in the future.
