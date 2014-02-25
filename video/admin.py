"""Admin config"""
from video.models import Video, Profile
from django.contrib import admin


class VideoAdmin(admin.ModelAdmin):
    model = Video
    list_display = ("__unicode__", "user", "state", "host")

admin.site.register(Video, VideoAdmin)
admin.site.register(Profile)