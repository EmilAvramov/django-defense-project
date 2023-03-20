from django.contrib import admin
from .models import User, Guest

# Register your models here.
admin.site.register(User)
admin.site.register(Guest)