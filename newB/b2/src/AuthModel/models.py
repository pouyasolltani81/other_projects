from django.db import models
from django.utils import timezone
from datetime import timedelta
from UserModel.models import User
import hashlib
from app import settings
from functools import wraps
from django.http import JsonResponse
from LogModel.log_handler import print_log

def api_get_hash(message, len=32):
    hash = hashlib.sha256(str(message).encode()).hexdigest()[:len]
    return hash

def user_credential(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        auth_token = request.headers.get('Authorization')

        if not auth_token:
            return JsonResponse({'error': 'Access denied: user not authenticated and user token is missing.', 'return': False})
        
        try:
            ua = UserAuth.objects.get(token=auth_token)
            
        except Exception as e:
            return JsonResponse({'error': 'Access denied: invalid user token. ' + str(e), 'return': False})
        
        
        request.user = ua.user
        return view_func(request, *args, **kwargs)
    
    return wrapper
#######################################################################
def app_credential(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        
        app_token = request.headers.get('Authorization')

        if not app_token:
            return JsonResponse({'error': 'Access denied: app token is missing.', 'return': False})

        if app_token != settings.APP_TOKEN:        
            return JsonResponse({'error': 'Access denied: invalid app token.', 'return': False})
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
#######################################################################

class UserAuth(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, related_name='user_auth', on_delete=models.CASCADE)
    token = models.CharField(max_length=32, null=False, blank=False) # to get service

    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'User Auth'
        verbose_name_plural = 'User Auth'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user}'
    
    #####################################################################
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = api_get_hash(f'{self.user.id}/{timezone.now().second}/token', len=32)
            self.expired_at = timezone.now() + timedelta(hours=720)

        super().save(*args, **kwargs)
    #####################################################################
    @staticmethod
    def check_user_auth(self, request, token):
        try:
            ua = UserAuth.objects.filter(token=token).first()
            if not ua:
                return {'return':False, 'message':'Token Invalid'}
            
            if ua.expired_at < timezone.now():
                return {'return':False, 'message':'Token Expired.'}
            
            if request.user.id != ua.user.id:
                return {'return':False, 'message':'Token is valid and user not logged in'}
            
            if request.user.is_authenticated:
                return {'return':True, 'message':'Token is valid and user logged in', 'expired_at':ua.expired_at}
            
            return {'return':False, 'message':'Token is valid and user not logged in'}
        
        except Exception as e:
            print_log(user=None, level='return', message=str(e), exception_type='Exception', stack_trace=str(e), file_path='AuthModel/models.py', line_number=0)
            return {'return':False, 'error':str(e)}

