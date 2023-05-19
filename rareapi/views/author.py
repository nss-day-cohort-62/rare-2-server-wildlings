from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Author

class AuthorView(ViewSet):
    """Rare Author view"""
    def list(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for authors"""
    class Meta:
        model = Author
        fields = ('id', 'full_name', 'bio', 'created_on', 'active')
