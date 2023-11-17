from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from .documents import DocumentTodo
from .models import Todo, Category, Subscriber
from .tasks import send_email


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class TodoSerializerForRetrieve(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class TodoSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        subscribers = Subscriber.objects.all().values('email')
        subscriber_emails = [email['email'] for email in list(subscribers)]
        print(subscriber_emails)
        todo = Todo.objects.create(**validated_data)
        todo_serializer = TodoSerializerForRetrieve(todo)
        send_email.delay(subscriber_emails, todo_serializer.data)
        return todo

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


class SlugSerializer(serializers.Serializer):
    slug = serializers.CharField()


class TodoDocumentSerializer(DocumentSerializer):
    price = serializers.FloatField()

    def get_price(self, obj):
        return float(obj.price)

    class Meta:
        document = DocumentTodo
        fields = ('title', 'slug', 'description', 'price', 'color')


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'
