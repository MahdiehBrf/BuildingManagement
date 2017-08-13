from django.contrib import admin

# Register your models here.
from Manager.models import Manager, Request

admin.site.register(Manager)
admin.site.register(Request)