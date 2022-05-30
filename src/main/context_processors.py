from django.conf import settings


def settings_context(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'GOOGLE_ANALYTICS_TRACKING_ID': getattr(settings, 'GOOGLE_ANALYTICS_TRACKING_ID', None)
    }
