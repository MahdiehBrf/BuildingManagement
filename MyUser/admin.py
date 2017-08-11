from django.contrib import admin

# Register your models here.
from MyUser.models import Member

admin.site.register(Member)