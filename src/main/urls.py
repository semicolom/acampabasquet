from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from . import views

admin.site.site_header = "Acampabàsquet"
admin.site.site_title = "Acampabàsquet"
admin.site.index_title = ''

urlpatterns = [
    path('{}/'.format(settings.ADMIN_URL), admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('grups/', views.GroupsView.as_view(), name='groups'),
    path('grups/<int:pk>', views.GroupDetailView.as_view(), name='group-detail'),
    path('grups/equips/<int:pk>', views.TeamView.as_view(), name='team'),
]

# On development serve media and static files using django
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django debug toolbar URLs
if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
