from django.contrib import admin
from django.urls import path, include

from app.content.v1.views import ContentView, ContentDetailView

urlpatterns = [
    path("content/", ContentView.as_view(), name="content"),
    path("content/<int:pk>/", ContentDetailView.as_view(), name="content_detail"),
    path("admin/", admin.site.urls),
    path("v1/", include("app.content.v1.urls")),
    path("v1/", include("app.user.v1.urls")),
    path("accounts/", include("allauth.urls")),
]
