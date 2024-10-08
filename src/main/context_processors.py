from django.conf import settings


def settings_context(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'MEDIA_URL': settings.MEDIA_URL,
    }
