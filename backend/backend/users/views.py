from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.core.utils.tokens import generate_token
from backend.users.serializers import UserSerializer

User = get_user_model()


class GetOTPView(APIView):
    def post(self, request: Request) -> Response:
        while True:
            token = generate_token()
            if not cache.get(token):
                break

        key = f"otp_token.{token}"

        cache.set(key, request.user.pk, timeout=settings.OPT_TOKEN_TIMEOUT)
        return Response({"token": token})


class RegistrationView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
