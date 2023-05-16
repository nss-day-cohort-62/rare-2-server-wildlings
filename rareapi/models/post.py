from django.db import models

class Post(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="category_posts")
    title = models.CharField(max_length=50)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=1000000)
    content = models.CharField(max_length=250)
