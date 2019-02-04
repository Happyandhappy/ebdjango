from django.contrib import admin

from . models import Task, Step


class StepInline(admin.StackedInline):
    model = Step


class TaskAdmin(admin.ModelAdmin):
    inlines = [StepInline,]


admin.site.register(Task, TaskAdmin)
