from django.contrib import admin

from .models import Employee, ControlPanel, Profile, RoomCondition


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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo' ]
    ordering = ['user']


@admin.register(RoomCondition)
class RoomConditionAdmin(admin.ModelAdmin):
    list_display = ['created', 'temperature', 'humidity', 'soilmoisture' ]
    ordering = ['created']