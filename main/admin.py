from django.contrib import admin
from django.contrib.auth.models import User, Group
from . import models

admin.site.site_header = "Gajah Petir Dashboard"
admin.site.site_title = "Gajah Petir"

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['time_order']
    search_fields = ["userid", "zoneid", "status"]
    list_display = ["id", "userid", "zoneid", "item", "status"]
    ordering = ["-time_order"]
    readonly_fields = ['id', 'userid', 'zoneid', 'item', 'time_order', 'pay_with', 'nowa']


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(models.Item)
admin.site.register(models.Payment)
admin.site.register(models.Order, OrderAdmin)