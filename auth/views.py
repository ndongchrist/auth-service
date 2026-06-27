"""Auth API — the only service that ISSUES JWTs.

register/login/refresh are public (Kong does not require a token on /auth/*).
The access token's `user_id` claim is what Kong validates at the edge and
injects downstream as X-User-Id. Tokens are HS256-signed with the shared
DJANGO_SECRET_KEY (the same secret Kong's jwt plugin is configured with).
"""
from __future__ import annotations

from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def register(request: Request) -> Response:
    ser = RegisterSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    data = ser.validated_data
    if User.objects.filter(username=data["username"]).exists():
        return Response({"detail": "username already taken"}, status=400)
    user = User.objects.create_user(
        username=data["username"], email=data.get("email", ""), password=data["password"]
    )
    refresh = RefreshToken.for_user(user)
    return Response(
        {"user_id": user.id, "access": str(refresh.access_token), "refresh": str(refresh)},
        status=201,
    )
