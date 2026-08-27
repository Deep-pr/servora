from .models import AuditLog


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if self._should_log(request, response):
            AuditLog.objects.create(
                actor=request.user,
                action=f'{request.method} {request.path}',
                target_model='http_request',
                target_id='',
                metadata={'status_code': response.status_code},
                ip_address=self._client_ip(request),
            )
        return response

    def _should_log(self, request, response):
        user = getattr(request, 'user', None)
        return (
            user is not None
            and user.is_authenticated
            and request.method in {'POST', 'PUT', 'PATCH', 'DELETE'}
            and response.status_code < 500
        )

    def _client_ip(self, request):
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
