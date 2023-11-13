import datetime
from datetime import timedelta

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Search
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveAPIView

from accounts.permissions import AdminPermission
from .models import Todo, Category
from .serializers import TodoSerializer, CategorySerializer, QuerySerializer, TodoSerializerForFilter, SlugSerializer


# class TodoAPIView(GenericAPIView):
#     permission_classes = ()
#     serializer_class = TodoSerializer
#
#     def get(self, request):
#         todos = Todo.objects.all()
#         # todos = Todo.objects.filter(Q(expires_at__gte=datetime.datetime.now() - timedelta(days=3)) & Q(expires_at__lte=datetime.datetime.now()))
#         todos_data = TodoSerializer(todos, many=True)
#         return Response(todos_data.data)

class TodoAPIView(ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = ()


# class CreateTodoAPIView(GenericAPIView):
#     permission_classes = (AdminPermission,)
#     serializer_class = TodoSerializer

    # def post(self, request):
    #     todo_serializer = TodoSerializer(data=request.data)
    #     todo_serializer.is_valid(raise_exception=True)
    #     todo_serializer.save()
    #     return Response(todo_serializer.data)

class CreateTodoAPIView(CreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (AdminPermission,)


# class TodoUpdateAPIView(GenericAPIView):
#     serializer_class = TodoSerializer
#
#     def get(self, request, pk):
#         todo = Todo.objects.get(pk=pk)
#         todo_serializer = TodoSerializer(todo)
#         return Response(todo_serializer.data)
#
#     def put(self, request, pk):
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         todo = Todo.objects.get(pk=pk)
#         todo.title = title
#         todo.description = description
#         todo.expires_at = datetime.datetime.now()
#         todo.save()
#         todo_serializer = TodoSerializer(todo)
#         return Response(todo_serializer.data)
#
#     def patch(self, request, pk):
#         title = request.POST.get('title', None)
#         description = request.POST.get('description', None)
#         todo = Todo.objects.get(pk=pk)
#         if title:
#             todo.title = title
#         if description:
#             todo.description = description
#         todo.save()
#         todo_serializer = TodoSerializer(todo)
#         return Response(todo_serializer.data)
#
#     def delete(self, request, pk):
#         Todo.objects.get(pk=pk).delete()
#         return Response(status=204)

class TodoUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)


# class TodoDetailAPIView(GenericAPIView):
#     permission_classes = ()
#     serializer_class = TodoSerializer
#
#     def get(self, request, slug):
#         try:
#             todo = Todo.objects.get(slug=slug)
#         except Todo.DoesNotExist:
#             return Response({'success': False}, status=404)
#         todo_serializer = TodoSerializer(todo)
#         return Response(todo_serializer.data)
class TodoDetailAPIView(RetrieveAPIView):
    serializer_class = TodoSerializer
    permission_classes = ()

    @swagger_auto_schema(query_serializer=SlugSerializer)
    def get(self, request):
        slug = self.request.query_params.get('slug', None)
        if slug is not None:
            todo = Todo.objects.filter(slug=slug).first()
        else:
            todo = Todo.objects.first()
        todo_serializer = self.get_serializer(todo)
        return Response(todo_serializer.data)


class SearchAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = CategorySerializer

    @swagger_auto_schema(query_serializer=QuerySerializer)
    def get(self, request):
        query = request.GET.get('query')
        base_categories = Category.objects.filter(Q(name__icontains=query) & Q(parent=None)).values('tree_id')
        categories = Category.objects.filter(tree_id__in=base_categories)
        # categories_data = []
        # for category in categories:
        #     cate = Category.objects.filter(tree_id=category.tree_id)
        #     category_serializer = CategorySerializer(cate, many=True)
        #     categories_data.append(category_serializer.data)
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)


class TodoFilterAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = TodoSerializer

    @swagger_auto_schema(query_serializer=TodoSerializerForFilter)
    def get(self, request):
        start = request.GET.get('start', 0)
        end = request.GET.get('end', 999999999999)
        name = request.GET.get('name', '')
        category_name = request.GET.get('category_name', '')
        date = request.GET.get('date', None)
        color = request.GET.get('color', '')

        price_query = Q(price__gte=start) & Q(price__lte=end)

        if name == '':
            title_query = Q()
        else:
            title_query = Q(title__icontains=name)

        if not date:
            date_query = Q()
        else:
            date_query = Q(expires_at=date)

        if color == '':
            color_query = Q()
        else:
            color_query = Q(color=color)

        q = price_query & title_query & date_query & color_query

        todos = Todo.objects.filter(q)
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data)
