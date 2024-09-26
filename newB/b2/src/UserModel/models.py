
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

class User(AbstractUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=150, default='', blank=True)
    email = models.CharField(max_length=100, default='', unique=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.email} ({self.username})'
    
    def save(self, *args, **kwargs):

        if not self.pk and not self.is_superuser: 
            self.set_password(self.password)

        super().save(*args, **kwargs)

        from AuthModel.models import UserAuth
        userauth = UserAuth.objects.get_or_create(user=self)
        

    def auth(self):
        from AuthModel.models import UserAuth
        return UserAuth.objects.filter(user=self).first()
    
    @classmethod
    def get_user_auth(cls, email, password):

        user = cls.objects.filter(email=email).first()

        if not user:
            return None, {'return':False, 'error': 'Invalid email.'}
        
        if not user.check_password(password):
            return None, {'return':False, 'error': 'Invalid password.'}
        
        if not user.is_active:
            return None, {'return':False, 'error': 'User is not active.'}
        
        user_auth = user.auth()
        if user_auth.expired_at and user_auth.expired_at < timezone.now():
            return None, {'return':False, 'error': 'Token expired.'}
        
        return user, {'return': True}
    #########################################################################