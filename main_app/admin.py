from django.contrib import admin
from .models import *

# Register your models here.
class Admins(admin.ModelAdmin):
    list_display = ('title', 'user')

admin.site.register(Error, Admins)
admin.site.register(Comment)
admin.site.register(Screenshot)
