from rest_framework import serializers


class CurrentInstanceDefault(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        return serializer_field.context["view"].get_object()
