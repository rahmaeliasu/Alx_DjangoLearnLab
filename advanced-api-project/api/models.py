from django.db import models


# ---------------------------------------------------------
# Author Model
# ---------------------------------------------------------
# This model represents an author in the system.
# It only stores the author's name.
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ---------------------------------------------------------
# Book Model
# ---------------------------------------------------------
# Each book has:
#  - a title
#  - a publication year
#  - a link to a specific Author
#
# The ForeignKey creates a ONE-TO-MANY relationship:
# One Author ➝ Many Books
#
# CASCADE ensures that if an Author is deleted,
# all their books automatically get deleted.
#
# related_name="books" lets us access all books of
# an author using author.books.all()
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )

    def __str__(self):
        return self.title
