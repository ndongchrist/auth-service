from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

# Kong routes /auth/* here with strip_path → paths relative to root.
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
]
