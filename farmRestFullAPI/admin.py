from django.contrib import admin

from .models import Employee,ControlPanel


# Register your models here.
@admin.register(Employee)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'slug', 'dob', 'email', 'created']
    list_filter = ['author', 'created', 'email']
    search_fields = ['userName']
    prepopulated_fields = {'slug': ('userName',)}
    ordering = ['created']


@admin.register(ControlPanel)
class ControlPanelAdmin(admin.ModelAdmin):
    list_display = ['author', 'created', 'hasFan', 'hasPump', 'hasLed']
    ordering = ['created']