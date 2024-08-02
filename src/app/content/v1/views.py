from rest_framework import viewsets, mixins

from app.content.models import Content
from app.content.v1.serialziers import ContentSerializer


class ContentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = []

    def get_queryset(self):
        print("get_queryset")
        return super().get_queryset()

    def get_serializer_context(self):
        print("get_serializer_context")
        return super().get_serializer_context()

    def get_serializer(self, *args, **kwargs):
        print("get_serializer")
        return super().get_serializer(*args, **kwargs)

    def get_object(self):
        print("get_object")
        return super().get_object()
