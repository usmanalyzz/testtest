from django.db import models

class Product(models.Model):
    logo = models.ImageField(upload_to='media/logo/')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/screenshots/')
    view_count = models.PositiveIntegerField(default=0)
    save_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
