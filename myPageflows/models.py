from django.db import models

class Product(models.Model):
    logo = models.ImageField(upload_to='media/logo/')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/screenshots/')
    view_count = models.PositiveIntegerField(default=0)
    save_count = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title


class UserFlow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='user_flows')
    category = models.CharField(max_length=100)
    video = models.FileField(upload_to='media/videos/')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/screenshots/')
    logo = models.ImageField(upload_to='media/logo/', null=True)
    view_count = models.PositiveIntegerField(default=0)
    save_count = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.view_count:
            self.view_count = self.product.view_count
        super().save(*args, **kwargs)





    def __str__(self):
        return self.name

class Screenshot(models.Model):
    user_flow = models.ForeignKey(UserFlow, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='media/screenshots/')

    def __str__(self):
        return f"Screenshot for {self.user_flow.name}"