from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'assigned_to', 'created_by', 'due_date', 'worked_hours', 'created_at')
    list_filter = ('status', 'assigned_to', 'created_by', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username', 'created_by__username')
    date_hierarchy = 'due_date'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Basic Info", {
            'fields': ('title', 'description', 'status')
        }),
        ("People", {
            'fields': ('assigned_to', 'created_by')
        }),
        ("Timeline", {
            'fields': ('due_date', 'created_at', 'updated_at')
        }),
        ("Completion Info", {
            'fields': ('completion_report', 'worked_hours')
        }),
    )

