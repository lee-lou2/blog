from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

from app.content.v1.views import ContentView, ContentDetailView, ContentEditView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("404/", lambda request: HttpResponse("Not Found", status=404)),
]

urlpatterns += [
    path("accounts/", include("allauth.urls")),
    path("", ContentView.as_view(), name="content"),
    path("content/edit/", ContentEditView.as_view(), name="content_edit"),
    path("content/<int:pk>/", ContentDetailView.as_view(), name="content_detail"),
]

urlpatterns += [
    path("v1/content/", include("app.content.v1.urls")),
    path("v1/user/", include("app.user.v1.urls")),
]
