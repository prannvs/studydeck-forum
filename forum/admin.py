from django.contrib import admin
from .models import Thread, Reply, Category, Course, Resource, Tag, Report

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Course)
admin.site.register(Resource)
admin.site.register(Thread)
admin.site.register(Reply)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('thread', 'reporter', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason') # Filter by Pending/Resolved
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        queryset.update(status='RESOLVED')