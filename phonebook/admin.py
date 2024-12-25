from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin
from django.utils.html import format_html
from .models import Department, CityPhoneNumber, Employee

@admin.register(Department)
class DepartmentAdmin(DraggableMPTTAdmin, ImportExportModelAdmin):
    list_display = (
        'tree_actions', 'indented_title', 'name_ru', 'name_kk', 'type', 'number', 'parent',
        'created_at', 'created_by', 'updated_at', 'updated_by', 'is_deleted_colored', 'deleted_at', 'deleted_by'
    )
    list_display_links = ('indented_title', 'name_ru', 'name_kk')
    list_filter = ('type', 'created_by', 'updated_by', 'is_deleted')
    search_fields = ('name_ru', 'name_kk')

    def is_deleted_colored(self, obj):
        if obj.is_deleted:
            return format_html('<span style="color: red;">{}</span>', obj.is_deleted)
        return obj.is_deleted

    is_deleted_colored.short_description = 'Удалено'


@admin.register(CityPhoneNumber)
class CityPhoneNumberAdmin(ImportExportModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = (
        'name_ru', 'name_kk', 'position_ru', 'position_kk', 'department', 'email', 'city_phone_number',
        'mobile_number', 'photo_thumbnail', 'created_at', 'created_by', 'updated_at', 'updated_by',
        'is_deleted_colored', 'deleted_at', 'deleted_by'
    )
    list_display_links = ('name_ru', 'name_kk')
    list_filter = ('department', 'created_by', 'updated_by', 'is_deleted')
    search_fields = ('name_ru', 'name_kk',)

    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
        return "Нет фото"

    photo_thumbnail.short_description = "Фото"

    def is_deleted_colored(self, obj):
        if obj.is_deleted:
            return format_html('<span style="color: red;">{}</span>', obj.is_deleted)
        return obj.is_deleted

    is_deleted_colored.short_description = 'Удалено'
