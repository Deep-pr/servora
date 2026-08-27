from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .models import AuditLog
from .services import analytics_chart_data, data_insights, platform_metrics


@staff_member_required
def analytics_dashboard(request):
    return render(request, 'analytics/dashboard.html', {
        'metrics': platform_metrics(),
        'charts': analytics_chart_data(),
        'insights': data_insights(),
    })


@staff_member_required
def audit_logs(request):
    logs = AuditLog.objects.select_related('actor')[:100]
    return render(request, 'analytics/audit_logs.html', {'logs': logs})

# Create your views here.
