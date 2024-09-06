from django.db import models

class TestModel(models.Model):
    test_number = models.CharField(default='', max_length=15)
    

    def __str__(self):
        return self.test_number