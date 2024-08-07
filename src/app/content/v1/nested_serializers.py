from rest_framework import serializers

from app.content.models import ContentComment, ContentTag


class ContentCommentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentComment
        fields = "__all__"


class ContentTagNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentTag
        fields = "__all__"
