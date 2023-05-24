from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Author, Category, Tag
from rest_framework.decorators import action


class PostView(ViewSet):
    """Rare Post view"""

    def list(self, request):
        posts = Post.objects.all()
        author = Author.objects.get(user=request.auth.user)
        poster = request.query_params.get('_user', None)

        if poster is not None:
            posts = posts.filter(author_id=author.id)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        author = Author.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category_id"])
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author, category=category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.category = Category.objects.get(pk=request.data["category_id"])
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        # post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.tags.set(request.data["tags"])
        post.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def tag_post(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        tag = Tag.objects.get(request.data['tag']['id'])
        post = Post.objects.get(pk=pk)
        post.tags.add(tag)
        return Response({'message': 'Tagged'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def untag_post(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        tag = Tag.objects.get(request.data['tag']['id'])
        post = Post.objects.get(pk=pk)
        post.tags.remove(tag)
        return Response({'message': 'Untagged'}, status=status.HTTP_204_NO_CONTENT)

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'publication_date',
            'image_url',
            'content',
            'tags'
        )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label')

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for Posts"""
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'author', 'category', 'title',
                  'publication_date', 'image_url', 'content', 'tags')
        depth= 1
