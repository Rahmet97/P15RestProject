from django.contrib import admin
from .models import Todo, Category, Subscriber


admin.site.register((Todo, Category, Subscriber))
