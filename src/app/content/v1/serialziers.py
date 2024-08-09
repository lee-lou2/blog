from rest_framework import serializers

from app.content.models import Content, ContentComment, ContentTag, ContentLike
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


class ContentLikeSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        instance, is_create = ContentLike.objects.get_or_create(
            content=kwargs["content"], user=kwargs["user"]
        )
        is_like = self.validated_data.get("is_like", True)
        before_is_like = instance.is_like if not is_create else False
        instance.is_like = is_like
        instance.save()
        if before_is_like != is_like and is_like:
            instance.content.like_count += 1
        elif before_is_like != is_like and not is_like:
            instance.content.like_count -= 1
        instance.content.save()
        return instance

    class Meta:
        model = ContentLike
        fields = ["is_like"]
