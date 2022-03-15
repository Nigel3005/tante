from django.contrib import admin
from .models import contact, GeeksModel


class contactAdmin(admin.ModelAdmin):
    list_display = ('name',)


class GeeksModelAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(GeeksModel, GeeksModelAdmin)
admin.site.register(contact, contactAdmin)
