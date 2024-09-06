from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from AuthModel.models import  check_auth_token
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, OpenApiResponse


@extend_schema(
    methods=['POST'],
    request={
    'application/json': {
        'type': 'object',
        'properties': {
            'm_data': {'type': 'number', 'format': 'float', 'minimum': 0, 'maximum': 100, 'example': 42.5},
            'n_data': {'type': 'string', 'minLength': 1, 'maxLength': 50, 'example': 'example_string'}
        },
        'required': ['m_data', 'n_data']
    }
    },
    #parameters=[
    #    OpenApiParameter(
    #        name='X-CSRFToken',
    #        type=OpenApiTypes.STR,
    #        location=OpenApiParameter.HEADER,
    #        required=True,
    #        description='CSRF Token'
    #    ),
    #],
    responses={
        200: {'description': 'OK', 'content': {'application/json': {'message':'ok'}} },
        401: {'description': 'OK', 'content': {'application/json': {'error':'not ok'}}},
    },
    description='Test1 API',
    summary='Test1 summary',
)
@api_view(['POST'])
@check_auth_token
#@permission_classes((AllowAny,))
def Test1(request):
    m = request.data.get('m_data')
    n = request.data.get('n_data')
    
    return JsonResponse({'message': 'ok', 'm data':m, 'n data':n})



@extend_schema(
    methods=['GET'],
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'key_data': {'type':'number', 'format':'float'},
            },
        }
    },
    responses={
        200: {'description': 'OK', 'content': {'application/json': {}}},
    },
    description='Test2 API',
    summary='Test2 summary description',
)
@api_view(['GET'])
@permission_classes((AllowAny,))
def Test2(request,a_data):
    return JsonResponse({'message': 'ok', 'a_data':a_data})