from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack, get_user_model
from channels.consumer import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.security.websocket import WebsocketDenier
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache

User = get_user_model()


class OneTimeTokenMiddleware(BaseMiddleware):
    """Authenticate user using one-time token."""

    @database_sync_to_async
    def _authenticate(self, token: str) -> AbstractUser | None:

        user_pk = cache.get(f"otp_token.{token}")
        print(user_pk, f"otp_token.{token}")

        try:
            user = User.objects.get(pk=user_pk)
            cache.delete(f"otp_token.{token}")
            return user
        except:
            return None

    async def _authenticate_user(self, scope: dict) -> None:
        query_string = scope.get("query_string", "").decode()
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        if not token:
            return

        scope["user"] = await self._authenticate(token)

    async def __call__(self, scope, receive, send):
        """Middleware constructor - just takes inner application."""
        await self._authenticate_user(scope)

        if not scope.get("user", None):
            denier = WebsocketDenier()
            return await denier(scope, receive, send)

        return await super().__call__(scope, receive, send)


def OneTimeTokenMiddlewareStack(inner) -> OneTimeTokenMiddleware:
    """Wrap `AuthMiddlewareStack` with `OneTimeTokenMiddleware`."""
    return OneTimeTokenMiddleware(AuthMiddlewareStack(inner))
