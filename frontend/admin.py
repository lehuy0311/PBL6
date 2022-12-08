from django.contrib import admin
from .models import *


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'body', 'date']
    list_filter = ['user_id']


# Register your models here.
admin.site.register(History, HistoryAdmin)

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)