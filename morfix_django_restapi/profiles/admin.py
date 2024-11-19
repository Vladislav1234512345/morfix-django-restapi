from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.utils.safestring import mark_safe

from . import models


class ProfileImageAdmin(admin.ModelAdmin):
    fields = ["profile", "image", "uploaded_at", "is_main_image"]
    readonly_fields = ["image"]

    def image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}">')

class ProfileAdmin(GISModelAdmin):
    list_display = ('id', 'first_name', 'address')  # отображение полей ('id', 'first_name', 'location')
    search_fields = ('id', 'first_name', 'address') # поиск по полям ('id', 'first_name', 'location')

# Register your models here.


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.ProfileImage, ProfileImageAdmin)
admin.site.register(models.ProfileHobby)
admin.site.register(models.Hobby)
admin.site.register(models.Like)
