from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SiteUser)
admin.site.register(Notification)


class Users(admin.TabularInline):
    model = SiteUser
    readonly_fields = ('id',)
