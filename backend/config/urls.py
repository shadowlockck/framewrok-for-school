from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from apps.core.views import PublicSchoolHomeView
from apps.core.modules import module_urlpatterns

urlpatterns = [
    # Public School Website Home Page
    path('', PublicSchoolHomeView.as_view(), name='home'),

    # Django Admin
    path('admin/', admin.site.urls),

    # OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Modular School API Endpoints
    path('api/v1/core/', include('apps.core.urls')),
]
urlpatterns += module_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Панель керування сайтом школи"
admin.site.site_title = "School Framework CMS"
admin.site.index_title = "Управління контентом та обов'язковими документами закладу"
