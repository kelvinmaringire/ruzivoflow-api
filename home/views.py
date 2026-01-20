from django.http import FileResponse
from django.conf import settings
import os

def serve_spa(request, path=''):
    """Serve Vue SPA index.html for all non-API routes"""
    index_path = os.path.join(settings.BASE_DIR, 'dist', 'index.html')
    if os.path.exists(index_path):
        return FileResponse(open(index_path, 'rb'), content_type='text/html')
    from django.http import Http404
    raise Http404("SPA index.html not found")