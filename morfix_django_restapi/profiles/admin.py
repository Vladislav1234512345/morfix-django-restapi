from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from . import models

class ProfileAdmin(GISModelAdmin):
    list_display = ('id', 'first_name', 'address')  # отображение полей ('id', 'first_name', 'location')
    search_fields = ('id', 'first_name', 'address') # поиск по полям ('id', 'first_name', 'location')

# Register your models here.


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.ProfileImage)
admin.site.register(models.ProfileHobby)
admin.site.register(models.Hobby)
admin.site.register(models.Like)
