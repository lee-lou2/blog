from rest_framework import serializers

from app.content.models import Content


class ContentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

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

    class Meta:
        model = Content
        fields = "__all__"
