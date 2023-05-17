from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Author

class CommentView(ViewSet):
    """Rare Comment view"""
    def list(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        commenter = Author.objects.get(user=request.auth.user)
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(commenter=commenter)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.post = request.data["post"]
        comment.content = request.data["content"]
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'content', 'created_on')

class CommentSerializer(serializers.Serializer):
    """JSON serializer for comments"""
    class Meta:
        model = Comment
        fields = ('id', 'post', 'commenter', 'content', 'created_on')
