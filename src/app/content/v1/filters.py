from django_filters import rest_framework as filters

from app.content.models import Content


class ContentFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    tag_name = filters.CharFilter(method="filter_tag_name")

    def filter_tag_name(self, queryset, name, value):
        return queryset.filter(content_tags__name=value)

    class Meta:
        model = Content
        fields = ["title", "tag_name"]
