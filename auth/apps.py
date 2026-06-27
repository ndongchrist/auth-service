from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = "auth"
    # Distinct label so a service named after a Django builtin (e.g. "auth")
    # doesn't collide with django.contrib.* app labels.
    label = "auth_app"
