from django.contrib import admin
from core.models import App


class AppAdmin(admin.ModelAdmin):
    list_display = ["app_id", "name"]
    search_fields = ["app_id", "name"]


admin.site.register(App, AppAdmin)
