from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# ---------------------------------------------------------
# BookSerializer
# ---------------------------------------------------------
# Serializes all fields of the Book model.
# This is used whenever we want to send/receive book data
# through the API.
#
# Includes a custom validator to prevent adding books
# with publication years that are in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"  # title, publication_year, author

    # Custom validation for publication_year
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            return serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


# ---------------------------------------------------------
# AuthorSerializer
# ---------------------------------------------------------
# Serializes Author data AND includes a nested list of books.
#
# The 'books' field uses BookSerializer to serialize all books
# linked to this author through the ForeignKey relationship.
#
# This creates a nested JSON structure like:
# {
#   "name": "Ama Ata Aidoo",
#   "books": [
#       {"title": "...", "publication_year": 1991, "author": 2},
#       ...
#   ]
# }
#
# read_only=True ensures that you cannot create books directly
# through the AuthorSerializer. They must be created separately
# through the BookSerializer.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["name", "books"]
