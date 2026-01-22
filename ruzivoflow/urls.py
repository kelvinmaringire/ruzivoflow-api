from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.views.static import serve
import os  # Add this import

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .api import api_router
from home.views import serve_spa  # Import the SPA view

urlpatterns = [
    # API routes (must come before SPA catch-all)
    path('api/v2/', api_router.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Admin routes
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    
    # Other app routes
    path("search/", search_views.search, name="search"),
    path('accounts/', include('accounts.urls')),
    path('content_api/', include('content_api.urls')),
    path('node_editor/', include('node_editor.urls')),
    path('thedataeditor/', include('node_editor.urls')),  # Alias for frontend compatibility
    path('blog/', include('blog.urls')),
    
    # Serve static assets from www/assets at /assets/
    path('assets/<path:path>', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'www', 'assets')
    }),
    path('icons/<path:path>', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'www', 'icons')
    }),
    path('favicon.ico', serve, {
        'document_root': settings.BASE_DIR,
        'path': 'www/favicon.ico'
    }),
    path('favicon.png', serve, {
        'document_root': settings.BASE_DIR,
        'path': 'www/favicon.png'
    }),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# SPA catch-all: serve index.html for all other routes
# This must be last to catch all non-API routes
# Replace Wagtail's catch-all with SPA serving
urlpatterns += [
    path('', serve_spa, name='spa'),
    path('<path:path>', serve_spa),  # Catch-all for SPA routes
]