from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rareapi.models import Subscription, Author
from django.utils import timezone


class SubscriptionView(ViewSet):
    """Rare Subscription view"""
    def list(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(methods=['post'], detail=True)
    def subscribe(self, request, pk):
        """Post request for a user to subscribe to an author"""

        follower_user = request.user
        follower = Author.objects.get(user=follower_user)
        author = Author.objects.get(pk=pk)
        subscription = Subscription.objects.create(
            follower=follower,
            author=author,
            created_on=request.data.get("created_on", None),
            ended_on=request.data.get("ended_on", None)
        )
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def unsubscribe(self, request, pk):
        """Post request for a user to unsubscribe from an author"""
        try:
            subscription = Subscription.objects.get(pk=pk)
        except Subscription.DoesNotExist:
            return Response({'error': 'Subscription not found.'}, status=status.HTTP_404_NOT_FOUND)

        subscription.ended_on = timezone.now().date()
        subscription.save()
        return Response({'message': 'Unsubscribed'}, status=status.HTTP_204_NO_CONTENT)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'full_name')

class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for subscriptions"""
    follower = AuthorSerializer()
    author = AuthorSerializer()
    
    class Meta:
        model = Subscription
        fields = ('id', 'follower', 'author', 'created_on', 'ended_on')

