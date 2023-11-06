from django.contrib import admin
from .models import Role, UserRole


admin.site.register((Role, UserRole))
