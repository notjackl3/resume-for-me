import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
# AuthMiddleWareStack keeps django authentication for websocket connections (so that you can use request.user methods)
from channels.auth import AuthMiddlewareStack
import resume.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')


application = ProtocolTypeRouter({
    # if the request is http then we send it to the normal http handler
    "http": get_asgi_application(),
    # but if the request is websocket then we send it to the websocket consumers
    "websocket": AuthMiddlewareStack(
        URLRouter(
            resume.routing.websocket_urlpatterns
        )
    ),
})
