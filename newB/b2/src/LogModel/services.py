from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from AuthModel.models import user_credential
from .models import Log
from .log_handler import print_log
from .serializers import LogSerializer

@extend_schema(
    description='Retrieve logs from a given timestamp until now, or delete logs.',
    summary='Get or delete logs within a specific time range',
    methods=['POST', 'DELETE'],
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'timestamp': {'type':'string', 
                              'format':'date-time', 
                              'default': (timezone.now() - timezone.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), 
                              'description':'Start timestamp for log retrieval'},
            },
        }
    },
    responses={
        200: OpenApiResponse(
            response=LogSerializer(many=True),
            description='List of logs from the given timestamp until now',
        ),
        204: OpenApiResponse(
            description='No content. Logs deleted successfully.',
        ),
        404: OpenApiResponse(
            description='No logs found for the given timestamp.',
        ),
    },
)
@api_view(['POST', 'DELETE'])
@user_credential
def GetLogs(request):
    if request.method == 'POST':
        timestamp = request.data.get('timestamp', None)
        try:
            if timestamp:
                aware_timestamp = timezone.make_aware(timezone.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
                logs = Log.objects.filter(timestamp__gte=aware_timestamp)
            else:
                logs = Log.objects.filter(timestamp__gte=timezone.now() - timezone.timedelta(days=1))
            
            return JsonResponse({'return': True, 'logs': LogSerializer(logs, many=True).data})
        except Exception as e:
            print_log(request.user, 'error', str(e))
            return JsonResponse({'return': False, 'error': str(e)})

    elif request.method == 'DELETE':
        timestamp = request.data.get('timestamp', None)
        try:
            if timestamp:
                aware_timestamp = timezone.make_aware(timezone.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
                deleted_count, _ = Log.objects.filter(timestamp__gte=aware_timestamp).delete()
                if deleted_count > 0:
                    return JsonResponse({'return': True, 'message': 'Logs deleted successfully.'}, status=204)
                else:
                    return JsonResponse({'return': False, 'error': 'No logs found for the given timestamp.'}, status=404)
            else:
                # Delete all logs
                Log.objects.all().delete()
                return JsonResponse({'return': True, 'message': 'All logs deleted successfully.'}, status=204)
        except Exception as e:
            print_log(request.user, 'error', str(e))
            return JsonResponse({'return': False, 'error': str(e)})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
