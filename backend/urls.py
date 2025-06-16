from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse  # 👈 For root view

# 👇 Optional root view
def root_view(request):
    return JsonResponse({
        "message": "Welcome to the API",
        "endpoints": ["/api/public/", "/api/register/", "/api/token/"]
    })

urlpatterns = [
    path("", root_view),  # ✅ Root URL (http://127.0.0.1:8000/)
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("core.urls")),  # Core app routes (like /api/public/)
]
