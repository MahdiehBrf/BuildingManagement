from django.contrib import admin

# Register your models here.
from Resident.models import Resident, Receipt, PayByBank, PayByAccount, Account, Reserve

admin.site.register(Resident)
admin.site.register(Receipt)
admin.site.register(PayByAccount)
admin.site.register(PayByBank)
admin.site.register(Account)
admin.site.register(Reserve)

