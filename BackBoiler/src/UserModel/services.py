from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import  AllowAny
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse
from .models import User

@extend_schema(
    description='With email and password get auth token to use services',
    summary='user to use services should login or has a auth token in request header',
    methods=['POST'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {'type':'string', 'default': ''},
                'password': {'type':'string', 'default': ''},
            },
           'required': ['username','password']
        }
    },
    responses={
        200: OpenApiResponse(
            response={'return': 'boolean'},
            description='',
        ),
    },
)
@api_view(['POST'])
@permission_classes((AllowAny,))
def GetUserToken(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user, res = User.get_user_auth(email=email, password=password)
        if user:
            return JsonResponse({'return':True, 'message':'User valid to use services', 'username':user.username, 'email':user.email, 'token':user.auth().token})
        else:
            return JsonResponse({'return':False, 'message':'User auth invalid: ' + res['error']})
    except Exception as e:
        return JsonResponse({'return':False, 'error':str(e)})