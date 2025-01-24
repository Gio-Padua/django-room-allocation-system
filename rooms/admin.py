from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

class ResidentAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    
    export_form_class = ExportForm
    list_display = ('lname','fname', 'address', 'family_size', 'priority','priority_members', 'priority_category',  'assigned', 'date')
    search_fields = ('lname','fname', 'address',)  # Optional: Add fields for searching residents
    list_filter = ('address', 'priority', 'priority_members','lname','fname', 'address','assigned')
admin.site.register(Resident, ResidentAdmin)

class RoomAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ('name', 'building', 'capacity', 'priority')
    search_fields = ('name', 'building')
    list_filter = ('capacity', 'priority')


class AllocationAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ('resident',  'room', 'date')
    search_fields = ('resident__lname','resident__fname', 'room__name')  # Search by related model fields

admin.site.register(Room, RoomAdmin)
admin.site.register(Allocation, AllocationAdmin)

