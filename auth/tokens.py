"""JWT issuance with an `iss` claim.

Kong's jwt plugin identifies the signing credential by the token's `iss` claim
(key_claim_name=iss) and verifies the HS256 signature with that credential's
secret — which is the shared DJANGO_SECRET_KEY. So every token we mint must
carry iss = JWT_ISSUER. SimpleJWT copies refresh-token claims onto the derived
access token, so stamping the refresh is enough.
"""
from __future__ import annotations

from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

ISSUER = getattr(settings, "JWT_ISSUER", "ecommerce-auth")


def issue_for_user(user) -> tuple[str, str]:
    refresh = RefreshToken.for_user(user)
    refresh["iss"] = ISSUER
    return str(refresh.access_token), str(refresh)


class IssuerTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["iss"] = ISSUER
        return token
