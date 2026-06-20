from django.contrib import admin

from .models import User, Application, Review


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "transport", "payment_type", "status", "time_start")
    list_filter = ("status", "transport", "payment_type")
    search_fields = ("user__username", "user__full_name")
    list_editable = ("status",)
    ordering = ("-id",)
    list_per_page = 20


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "application", "content")
    search_fields = ("user__username", "content")
    list_per_page = 20


admin.site.register(User)