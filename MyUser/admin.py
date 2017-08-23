from django.contrib import admin

# Register your models here.
from MyUser.models import Member, Message

admin.site.register(Member)
admin.site.register(Message)
