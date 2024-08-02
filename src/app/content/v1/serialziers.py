from rest_framework import serializers

from app.content.models import Content


class ContentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return "test : " + obj.title

    class Meta:
        model = Content
        fields = "__all__"
