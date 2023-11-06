import datetime

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import AdminPermission
from .models import Todo, Category
from .serializers import TodoSerializer, CategorySerializer


class TodoAPIView(APIView):
    permission_classes = ()

    def get(self, request):
        todos = Todo.objects.all()
        todos_data = TodoSerializer(todos, many=True)
        return Response(todos_data.data)


class CreateTodoAPIView(APIView):
    permission_classes = (AdminPermission,)

    def post(self, request):
        todo_serializer = TodoSerializer(data=request.data)
        todo_serializer.is_valid(raise_exception=True)
        todo_serializer.save()
        return Response(todo_serializer.data)


class TodoUpdateAPIView(APIView):

    def get(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo_serializer = TodoSerializer(todo)
        return Response(todo_serializer.data)

    def put(self, request, pk):
        title = request.POST.get('title')
        description = request.POST.get('description')
        todo = Todo.objects.get(pk=pk)
        todo.title = title
        todo.description = description
        todo.expires_at = datetime.datetime.now()
        todo.save()
        todo_serializer = TodoSerializer(todo)
        return Response(todo_serializer.data)

    def patch(self, request, pk):
        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        todo = Todo.objects.get(pk=pk)
        if title:
            todo.title = title
        if description:
            todo.description = description
        todo.save()
        todo_serializer = TodoSerializer(todo)
        return Response(todo_serializer.data)

    def delete(self, request, pk):
        Todo.objects.get(pk=pk).delete()
        return Response(status=204)


class TodoDetailAPIView(APIView):
    permission_classes = ()

    def get(self, request, slug):
        try:
            todo = Todo.objects.get(slug=slug)
        except Todo.DoesNotExist:
            return Response({'success': False}, status=404)
        todo_serializer = TodoSerializer(todo)
        return Response(todo_serializer.data)


class SearchAPIView(APIView):
    permission_classes = ()

    def get(self, request):
        query = request.GET.get('query')
        categories = Category.objects.filter(name__icontains=query) # & Q(parent=None))
        # categories_data = []
        # for category in categories:
        #     cate = Category.objects.filter(tree_id=category.id)
        #     category_serializer = CategorySerializer(cate)
        #     categories_data.append(category_serializer.data)
        # return Response(categories_data)
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)
