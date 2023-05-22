from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Tag

class TagView(ViewSet):
    """Rare Tag view"""
    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CreateTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label')

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label')
