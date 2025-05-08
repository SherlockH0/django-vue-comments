import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.project.settings")
django_asgi_app = get_asgi_application()
from backend.comments.routing import websocket_urlpatterns
from backend.core.middleware import OneTimeTokenMiddlewareStack

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            OneTimeTokenMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
