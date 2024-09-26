from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from UserModel.models import User
from .models import UserAuth

@extend_schema(
    description='',
    summary='Check user auth token, auth user hash shows session is valid or not. if session is invalid or expired then auth user hash was removed',
    methods=['POST'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'user_token': {'type': 'string', 'default': ''},
            },
            'required': ['user_token'],
        }
    },
    responses={
        200: {'return': True },
    },
)
@api_view(['POST'])
@permission_classes((AllowAny,))
def CheckUserAuth(request):
    try:
        user_token = request.data.get('user_token')
        
        ua = UserAuth().check_user_auth(request=request, token=user_token)
        return JsonResponse(ua)
    
    except Exception as e:
        return JsonResponse({'error': str(e),'return': False})    
    
