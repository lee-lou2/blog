from rest_framework import serializers

from app.content.models import ContentComment, ContentTag


class ContentCommentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentComment
        fields = (
            "id",
            "parent",
            "body",
            "user",
            "created_at",
        )


class ContentTagNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentTag
        fields = ("id", "name")
