from django.db import models
from django.utils import timezone
from UserModel.models import User

LEVEL_CHOICES = [
    ('error', 'Error'),
    ('warning', 'Warning'),
    ('urgent error', 'Urgent Error'),
    ('return', 'Return'),
    ('info', 'Info'),
]

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='error')
    message = models.TextField(default='')
    exception_type = models.CharField(max_length=255, default='')
    stack_trace = models.TextField(default='')
    file_path = models.CharField(max_length=255, default='')
    line_number = models.IntegerField(default=0)
    view_name = models.CharField(max_length=255, null=True, blank=True)
    

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.level}: {self.message}"