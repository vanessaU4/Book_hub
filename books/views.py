from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from django.http import Http404
from django.db.models import Q

class BookList(APIView):
    def get(self, request):
        books = Book.objects.all().order_by('-created_at')

        # Filters
        genre = request.query_params.get('genre')
        author = request.query_params.get('author')
        min_rating = request.query_params.get('min_rating')
        max_rating = request.query_params.get('max_rating')
        year_start = request.query_params.get('year_start')
        year_end = request.query_params.get('year_end')
        search = request.query_params.get('search')

        if genre and genre.lower() != "all genres":
            books = books.filter(genre__icontains=genre)
        if author:
            books = books.filter(author__icontains=author)
        if min_rating:
            books = books.filter(rating__gte=float(min_rating))
        if max_rating:
            books = books.filter(rating__lte=float(max_rating))
        if year_start:
            books = books.filter(publication_date__year__gte=int(year_start))
        if year_end:
            books = books.filter(publication_date__year__lte=int(year_end))
        if search:
            books = books.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(author__icontains=search)
            )

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Book created successfully",
                    "data": serializer.data
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Book updated successfully",
                    "data": serializer.data
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Book partially updated successfully",
                    "data": serializer.data
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(
            {"message": "Book deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    