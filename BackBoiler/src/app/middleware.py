import logging

logger = logging.getLogger('django')

class LogUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = 'Anonymous'
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        
       
        logger.info(f"User '{user}' accessed {request.method} {request.path}")

        response = self.get_response(request)
        return response
