from django.urls import path
from .views import TodoAPIView, TodoUpdateAPIView, CreateTodoAPIView, TodoDetailAPIView, SearchAPIView

urlpatterns = [
    path('todo', TodoAPIView.as_view(), name='todo'),
    path('todo/<str:slug>', TodoDetailAPIView.as_view(), name='todo_detail'),
    path('create-todo', CreateTodoAPIView.as_view(), name='create_todo'),
    path('todo-update/<int:pk>', TodoUpdateAPIView.as_view(), name='todo_update'),
    path('category-list', SearchAPIView.as_view(), name='categories'),
]
