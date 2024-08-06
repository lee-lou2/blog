from rest_framework import serializers

from app.content.models import Content, ContentComment, ContentTag
from app.content.v1.nested_serializers import ContentChildCommentSerializer


class ContentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentTag
        fields = "__all__"


class ContentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    tags = ContentTagSerializer(many=True, read_only=True, source="content_tags")

    def get_title(self, obj):
        # self.context
        return "test : " + obj.title

    def validate(self, attrs):
        return attrs

    def validate_title(self, data):
        return data

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def to_representation(self, instance):
        return super().to_representation(instance)

    def save(self, **kwargs):
        return super().save(**kwargs)

    class Meta:
        model = Content
        fields = "__all__"


class ContentCommentSerializer(serializers.ModelSerializer):
    child = ContentChildCommentSerializer(allow_null=True)

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        child_obj = ContentComment.objects.filter(parent=instance)
        serializer = ContentChildCommentSerializer(child_obj, many=True)
        resp["child"] = serializer.data
        return resp

    class Meta:
        model = ContentComment
        fields = "__all__"
