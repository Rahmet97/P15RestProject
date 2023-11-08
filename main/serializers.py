from rest_framework import serializers

from .models import Todo, Category


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    # parent = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()


class TodoSerializerForFilter(serializers.Serializer):
    name = serializers.CharField(required=False)
    category_name = serializers.CharField(required=False)
    start = serializers.FloatField(required=False)
    end = serializers.FloatField(required=False)
    color = serializers.CharField(required=False)
    date = serializers.DateTimeField(required=False)
