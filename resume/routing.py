from django.urls import re_path
from . import consumers

# these patterns are similar to urls.py but for websockets
websocket_urlpatterns = [
    # ws/pdf-preview/ is the endpoint that the browser connections to 
    re_path(r'ws/pdf-preview/$', consumers.PDFPreviewConsumer.as_asgi()),
]
