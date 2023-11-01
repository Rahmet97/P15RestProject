from django.urls import path
from .views import TodoAPIView, TodoUpdateAPIView

urlpatterns = [
    path('todo', TodoAPIView.as_view(), name='todo'),
    path('todo-update/<int:pk>', TodoUpdateAPIView.as_view(), name='todo_update')
]
