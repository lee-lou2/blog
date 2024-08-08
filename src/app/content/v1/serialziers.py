from rest_framework import serializers

from app.content.models import Content, ContentComment, ContentTag
from app.content.utils import format_time_ago
from app.content.v1.nested_serializers import (
    ContentCommentNestedSerializer,
)


class ContentSerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField())
    published_at = serializers.SerializerMethodField()

    def get_published_at(self, instance):
        return format_time_ago(instance.created_at)

    def to_representation(self, instance):
        instance.tags = instance.content_tags.all().values_list("name", flat=True)
        return super().to_representation(instance)

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        instance = super().create(validated_data)
        tag_objs = [ContentTag(name=tag, content=instance) for tag in tags]
        ContentTag.objects.bulk_create(tag_objs)
        return instance

    class Meta:
        model = Content
        fields = "__all__"


class ContentCommentSerializer(serializers.ModelSerializer):
    reply = ContentCommentNestedSerializer(
        allow_null=True, many=True, source="reply_comments"
    )

    class Meta:
        model = ContentComment
        fields = "__all__"
