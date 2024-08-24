from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

class ResidentAdmin(ModelAdmin):
    list_display = ('name', 'address', 'family_size', 'priority', 'assigned')
    search_fields = ('name', 'address')  # Optional: Add fields for searching residents
    list_filter = ('address', 'priority')
admin.site.register(Resident, ResidentAdmin)

class RoomAdmin(ModelAdmin):
    list_display = ('name', 'building', 'capacity', 'priority')
    search_fields = ('name', 'building')
    list_filter = ('capacity', 'priority')


class AllocationAdmin(ModelAdmin):
    list_display = ('resident', 'room', 'date')
    search_fields = ('resident__name', 'room__name')  # Search by related model fields

admin.site.register(Room, RoomAdmin)
admin.site.register(Allocation, AllocationAdmin)

