from django.contrib import admin
from core.models import App, Developer, Screenshot


class AppAdmin(admin.ModelAdmin):
    list_display = ["app_id", "name", "url"]
    search_fields = ["app_id", "name"]


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "url"]
    search_fields = ["email", "name"]


class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ["app", "url"]


admin.site.register(App, AppAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Screenshot, ScreenshotAdmin)
