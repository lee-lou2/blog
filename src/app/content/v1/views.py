from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from rest_framework import viewsets, mixins, pagination, response, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.content.models import Content, ContentComment
from app.content.v1.filters import ContentFilter
from app.content.v1.permissions import ContentUpdatePermission
from app.content.v1.serialziers import (
    ContentSerializer,
    ContentCommentSerializer,
    ContentLikeSerializer,
    ContentReportSerializer,
)


class UserProfileRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not hasattr(request.user, "profile"):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ContentView(LoginRequiredMixin, generic.TemplateView):
    template_name = "content/list.html"


class ContentEditView(LoginRequiredMixin, generic.TemplateView):
    template_name = "content/edit.html"


class ContentUpdateView(UserProfileRequiredMixin, generic.TemplateView):
    def get_context_data(self, **kwargs):
        pass


class ContentDetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = "content/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_id"] = self.kwargs.get("pk")
        return context


class ContentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Content.objects.filter(is_active=True)
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination
    filterset_class = ContentFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [ContentUpdatePermission()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-id")
        if self.action in ["list", "retrieve"]:
            queryset = queryset.exclude(content_reports__user=self.request.user)
        if self.action in ["create", "update", "partial_update"]:
            return queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.increase_view()
        return response.Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["PUT"], serializer_class=ContentLikeSerializer)
    def like(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=True, methods=["POST"], serializer_class=ContentReportSerializer)
    def report(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ContentCommentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    queryset = ContentComment.objects.all()
    serializer_class = ContentCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        content_id = self.kwargs.get("content_id")
        queryset = super().get_queryset()
        return queryset.filter(content_id=content_id).filter(parent__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
