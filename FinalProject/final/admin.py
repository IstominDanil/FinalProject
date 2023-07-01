from django.contrib import admin
from .models import Advertisement, Category, Reply

admin.site.register(Advertisement)
admin.site.register(Category)


# Register your models here.
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('text', 'final', 'user', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('user', 'text')

    def approve_reply(self, request, queryset):
        queryset.update(approve=True)


admin.site.register(Reply, ReplyAdmin)
