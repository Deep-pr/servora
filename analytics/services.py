from collections import Counter

from django.db.models import Avg, Count, Sum
from django.db.models.functions import ExtractHour, TruncMonth

from accounts.models import User
from bookings.models import Booking
from complaints.models import Complaint
from providers.models import ProviderProfile
from services.models import ServiceCategory


def platform_metrics():
    completed = Booking.objects.filter(status__in=[Booking.COMPLETED, Booking.REVIEWED])
    return {
        'total_users': User.objects.count(),
        'total_customers': User.objects.filter(role=User.CUSTOMER).count(),
        'total_providers': ProviderProfile.objects.count(),
        'verified_providers': ProviderProfile.objects.filter(verification_status=ProviderProfile.APPROVED).count(),
        'total_bookings': Booking.objects.count(),
        'completed_bookings': completed.count(),
        'cancelled_bookings': Booking.objects.filter(status=Booking.CANCELLED).count(),
        'active_bookings': Booking.objects.filter(status__in=[Booking.PENDING, Booking.ACCEPTED, Booking.CONFIRMED, Booking.ON_THE_WAY, Booking.WORK_STARTED]).count(),
        'average_booking_value': completed.aggregate(value=Avg('estimated_amount'))['value'] or 0,
        'total_booking_value': completed.aggregate(value=Sum('estimated_amount'))['value'] or 0,
        'average_rating': ProviderProfile.objects.aggregate(value=Avg('average_rating'))['value'] or 0,
        'open_complaints': Complaint.objects.filter(status__in=[Complaint.OPEN, Complaint.UNDER_REVIEW]).count(),
    }


def analytics_chart_data():
    booking_trends = Booking.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Count('id')).order_by('month')
    user_growth = User.objects.annotate(month=TruncMonth('date_joined')).values('month').annotate(total=Count('id')).order_by('month')
    service_popularity = ServiceCategory.objects.annotate(total=Count('provider_services__bookings')).order_by('-total')[:8]
    booking_status = Booking.objects.values('status').annotate(total=Count('id')).order_by('status')
    peak_hours = Booking.objects.annotate(hour=ExtractHour('scheduled_for')).values('hour').annotate(total=Count('id')).order_by('hour')
    location_counts = ProviderProfile.objects.values('base_location').annotate(total=Count('id')).order_by('-total')[:8]

    return {
        'booking_trends': {
            'labels': [_month_label(item['month']) for item in booking_trends],
            'values': [item['total'] for item in booking_trends],
        },
        'user_growth': {
            'labels': [_month_label(item['month']) for item in user_growth],
            'values': [item['total'] for item in user_growth],
        },
        'service_popularity': {
            'labels': [item.name for item in service_popularity],
            'values': [item.total for item in service_popularity],
        },
        'booking_status': {
            'labels': [item['status'].replace('_', ' ').title() for item in booking_status],
            'values': [item['total'] for item in booking_status],
        },
        'peak_hours': {
            'labels': [f"{item['hour']}:00" for item in peak_hours],
            'values': [item['total'] for item in peak_hours],
        },
        'locations': {
            'labels': [item['base_location'] or 'Unknown' for item in location_counts],
            'values': [item['total'] for item in location_counts],
        },
    }


def data_insights():
    most_requested = (
        ServiceCategory.objects.annotate(total=Count('provider_services__bookings'))
        .order_by('-total')
        .first()
    )
    status_counts = Counter(Booking.objects.values_list('status', flat=True))
    total_bookings = sum(status_counts.values()) or 1
    cancellation_rate = round((status_counts.get(Booking.CANCELLED, 0) / total_bookings) * 100, 1)
    top_provider = ProviderProfile.objects.order_by('-completed_jobs', '-average_rating').first()

    return {
        'most_requested_service': most_requested.name if most_requested else 'Not enough data',
        'cancellation_rate': cancellation_rate,
        'top_provider': top_provider.business_name if top_provider else 'Not enough data',
    }


def _month_label(value):
    if not value:
        return 'Unknown'
    return value.strftime('%b %Y')
