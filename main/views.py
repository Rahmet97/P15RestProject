import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Todo
from .serializers import TodoSerializer


class TodoAPIView(APIView):

    def get(self, request):
        todos = Todo.objects.all()
        todos_data = TodoSerializer(todos, many=True)
        return Response(todos_data.data)

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        todo = Todo.objects.create(
            title=title,
            description=description
        )
        todo.save()
        todo_serializer = TodoSerializer(todo)
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
