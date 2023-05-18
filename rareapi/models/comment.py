from django.db import models

class Comment(models.Model):

    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey("Author", on_delete=models.CASCADE, related_name='author_comments')
    content = models.CharField(max_length=250)
    created_on = models.DateField()
