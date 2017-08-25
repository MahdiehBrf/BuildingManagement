from django.contrib import admin

# Register your models here.
from MyUser.models import Member, Message


class MemberAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user']


admin.site.register(Member, MemberAdmin)
admin.site.register(Message)
