from django.urls import path, include
from .views import TodoAPIView, TodoUpdateAPIView, CreateTodoAPIView, TodoDetailAPIView, SearchAPIView, \
    TodoSearchViewSet, TodoFilterView, SubscribeAPIView
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register('todo-search', TodoSearchViewSet, basename='search_todo')

urlpatterns = [
    path('todo', TodoAPIView.as_view(), name='todo'),
    path('todo-slug', TodoDetailAPIView.as_view(), name='todo_detail'),
    path('create-todo', CreateTodoAPIView.as_view(), name='create_todo'),
    path('todo-update/<int:pk>', TodoUpdateAPIView.as_view(), name='todo_update'),
    path('category-list', SearchAPIView.as_view(), name='categories'),
    # path('filter', TodoFilterAPIView.as_view(), name='filter'),
    path('filter', TodoFilterView.as_view(), name='filter'),
    path('subscribe', SubscribeAPIView.as_view(), name='subscribe'),
    path('', include(router.urls))
    # path('search', TodoSearchViewSet.as_view(), name='search'),
]
