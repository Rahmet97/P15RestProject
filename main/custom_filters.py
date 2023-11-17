from django_filters import rest_framework as filters

from .models import Todo


class TodoFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Todo
        fields = ('title', 'slug', 'color')
