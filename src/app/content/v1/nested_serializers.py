from rest_framework import serializers

from app.content.models import ContentComment


class ContentChildCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentComment
        fields = "__all__"
