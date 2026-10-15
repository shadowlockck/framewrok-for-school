from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Modular School API Endpoints
    path('api/v1/core/', include('apps.core.urls')),
    path('api/v1/legal/', include('apps.legal.urls')),
    path('api/v1/admissions/', include('apps.admissions.urls')),
    path('api/v1/nutrition/', include('apps.nutrition.urls')),
    path('api/v1/safety/', include('apps.safety.urls')),
    path('api/v1/news/', include('apps.news.urls')),
    path('api/v1/schedule/', include('apps.schedule.urls')),
    path('api/v1/gallery/', include('apps.gallery.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Панель керування сайтом школи"
admin.site.site_title = "School Framework CMS"
admin.site.index_title = "Управління контентом та обов'язковими документами закладу"
