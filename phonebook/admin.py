from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Department, CityPhoneNumber, Employee

@admin.register(Department)
class DepartmentAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'name_ru', 'name_kk', 'type', 'number', 'parent')
    list_display_links = ('indented_title', 'name_ru', 'name_kk')
    list_filter = ('type',)
    search_fields = ('name_ru', 'name_kk')

@admin.register(CityPhoneNumber)
class CityPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position_ru', 'position_kk', 'department', 'email', 'city_phone_number', 'mobile_number')
    list_filter = ('department', 'position_ru', 'position_kk')
    search_fields = ('name', 'email', 'mobile_number')
