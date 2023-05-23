from django.db import models

class Subscription(models.Model):

    follower = models.ForeignKey("Author", on_delete=models.CASCADE, related_name='subscriptions')
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name='subscribers')
    created_on = models.DateTimeField(auto_now_add=True)
    ended_on = models.DateField(null=True)