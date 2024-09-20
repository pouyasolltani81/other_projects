from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)  
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    image_url = models.URLField(max_length=500)  
    product_url = models.URLField(max_length=500)  

    def __str__(self):
        return self.name
