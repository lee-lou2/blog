from rest_framework import serializers

from app.common.serializers import CurrentInstanceDefault
from app.content.models import (
    Content,
    ContentComment,
    ContentTag,
    ContentLike,
    ContentReport,
)
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

    def increase_view(self):
        self.instance.view_count += 1
        self.instance.save()

    class Meta:
        model = Content
        fields = (
            "id",
            "title",
            "body",
            "sub_title",
            "image_url",
            "created_at",
            "tags",
            "published_at",
        )


class ContentCommentSerializer(serializers.ModelSerializer):
    reply = ContentCommentNestedSerializer(
        allow_null=True, many=True, source="reply_comments"
    )

    class Meta:
        model = ContentComment
        fields = (
            "id",
            "content",
            "parent",
            "body",
            "user",
            "reply",
            "created_at",
        )


class ContentLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    content = serializers.HiddenField(default=CurrentInstanceDefault())

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        self.instance, _ = ContentLike.objects.get_or_create(
            content=data["content"], user=data["user"]
        )
        return data

    def update(self, instance, validated_data):
        is_like = validated_data.get("is_like", True)
        before_is_like = instance.is_like
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
        fields = ("is_like",)


class ContentReportSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    content = serializers.HiddenField(default=CurrentInstanceDefault())

    def validate(self, attrs):
        content = attrs.get("content")
        user = attrs.get("user")
        if ContentReport.objects.filter(content=content, user=user).exists():
            raise serializers.ValidationError("이미 신고한 콘텐츠입니다.")
        if content.user == user:
            raise serializers.ValidationError("본인의 콘텐츠는 신고할 수 없습니다.")
        return attrs

    class Meta:
        model = ContentReport
        fields = ("id", "user", "content", "message", "created_at")
