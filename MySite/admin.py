from django.contrib import admin

# Register your models here.
from MySite.models import Complex, Block, Board, Event, News, Facility, Unit

admin.site.register(Complex)
admin.site.register(Block)
admin.site.register(Board)
admin.site.register(Event)
admin.site.register(News)
admin.site.register(Facility)
admin.site.register(Unit)
