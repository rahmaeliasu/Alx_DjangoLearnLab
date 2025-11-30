## Book API Endpoints

- GET /api/books/ → List all books (public)
- GET /api/books/<id>/ → Retrieve a single book (public)
- POST /api/books/create/ → Create book (authenticated)
- PUT /api/books/<id>/update/ → Update book (authenticated)
- DELETE /api/books/<id>/delete/ → Delete book (authenticated)

All create/update operations validate publication_year to ensure it’s not in the future.

## Advanced Book Query Features

### Filtering
You can filter by:
- title
- author (id)
- publication_year

Example:
GET /api/books/?publication_year=1958

### Searching
Search across:
- book title
- author's name

Example:
GET /api/books/?search=achebe

### Ordering
Order by:
- title
- publication_year

Example:
GET /api/books/?ordering=-publication_year
