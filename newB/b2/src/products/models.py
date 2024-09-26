
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=50)
    image_url = models.URLField()
    product_url = models.URLField(unique=True)
    json_data = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
