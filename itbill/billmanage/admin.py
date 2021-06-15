from django.contrib import admin
from .models import *
# Register your models here.

class billAdmin(admin.ModelAdmin):
    model = bill
    list_display = ["billno","item","date","amount","remark","user"]
    ordering = ('date',)
    search_fields = ('item', 'billno','date')

admin.site.register(bill,billAdmin)