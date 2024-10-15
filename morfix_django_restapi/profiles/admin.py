from django.contrib import admin
from .models import Profile, ProfileImage, Hobby, ProfileHobby

# Register your models here.

admin.site.register(Profile)
admin.site.register(ProfileImage)
admin.site.register(ProfileHobby)
admin.site.register(Hobby)
