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
