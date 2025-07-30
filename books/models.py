from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    publication_date = models.DateField()
    description = models.TextField()
    cover_image = models.URLField()
    pages = models.PositiveIntegerField()
    isbn = models.CharField(max_length=20)
    language = models.CharField(max_length=30)
    publisher = models.CharField(max_length=100)
    price = models.FloatField()
    in_stock = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    