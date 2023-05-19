from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=155)
    created_on = models.DateField()
    active = models.BooleanField(default=True)

    @property # decorator
    def full_name(self):
        """Additional field to capture from the client"""
        return f'{self.user.first_name} {self.user.last_name}'
