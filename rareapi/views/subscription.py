from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rareapi.models import Subscription, Author

class SubscriptionView(ViewSet):
    """Rare Subscription view"""
    @action(methods=['post'], detail=True)
    def subscribe(self, request, pk):
        """Post request for a user to subscribe to an author"""

        follower = User.objects.get(user=request.auth.user)
        author = Author.objects.get(pk=pk)
        subscription = Subscription.objects.create(
            follower=follower,
            author=author,
            created_on=request.data["created_on"],
            ended_on=request.data["ended_on"]
        )
        serializer = SubscriptionSerializer(subscription)
        return Response({'message': 'Subscribed'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['update'], detail=True)
    def unsubscribe(self, request, pk):
        """Post request for a user to unsubscribe from an author"""
        """ subscription = Subscription.objects.get(pk=pk)
        subscription.delete()
        return Response({'message': 'Unsubscribed'}, status=status.HTTP_204_NO_CONTENT) """
        pass

class SubscriptionSerializer(serializers.Serializer):
    """JSON serializer for subscriptions"""
    class Meta:
        model = Subscription
        fields = ('id', 'follower', 'author', 'created_on', 'ended_on')
