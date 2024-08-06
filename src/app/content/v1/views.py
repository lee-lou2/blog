from rest_framework import viewsets, mixins, response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from app.content.models import Content, Author, ContentComment, ContentTag
from app.content.v1.serialziers import (
    ContentSerializer,
    ContentCommentSerializer,
    ContentTagSerializer,
)


class ContentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        author, _ = Author.objects.get_or_create(user=self.request.user, name="아무값")
        serializer.save(author=author)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author__user=self.request.user)

    def get_serializer_context(self):
        print("get_serializer_context")
        return super().get_serializer_context()

    def get_serializer(self, *args, **kwargs):
        print("get_serializer")
        return super().get_serializer(*args, **kwargs)

    def get_object(self):
        print("get_object")
        return super().get_object()

    @action(methods=["GET"], detail=True)
    def tags(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = ContentTagSerializer(obj.content_tags.all(), many=True)
        return response.Response({"tags": serializer.data})


class ContentCommentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    queryset = ContentComment.objects.all()
    serializer_class = ContentCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        content_id = self.request.query_params.get("content_id")
        queryset = super().get_queryset()
        return queryset.filter(content_id=content_id).filter(parent__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
