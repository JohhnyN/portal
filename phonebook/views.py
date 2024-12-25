from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib import messages
from django.db.models import ProtectedError
from django import forms
from django.utils import timezone
from .models import Department, Employee


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name_ru', 'name_kk', 'type', 'parent']


class DepartmentListView(ListView):
    model = Department
    template_name = "phonebook/department_list.html"
    context_object_name = "departments"

    def get_queryset(self):
        return Department.objects.filter(is_deleted=False)


class DepartmentDetailView(DetailView):
    model = Department
    template_name = "phonebook/department_detail.html"
    context_object_name = "department"

    def get_queryset(self):
        return Department.objects.filter(is_deleted=False)


class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Department
    template_name = "phonebook/department_form.html"
    fields = ["name_ru", "name_kk", "type", "parent"]
    success_url = reverse_lazy("department_list")
    permission_required = "phonebook.add_department"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Department
    template_name = "phonebook/department_form.html"
    fields = ["name_ru", "name_kk", "type", "parent"]
    success_url = reverse_lazy("department_list")
    permission_required = "phonebook.change_department"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Department
    template_name = "phonebook/department_confirm_delete.html"
    success_url = reverse_lazy("department_list")
    permission_required = "phonebook.delete_department"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.deleted_by = request.user
        self.object.deleted_at = timezone.now()
        self.object.save()
        return redirect(self.success_url)


class EmployeeListView(ListView):
    model = Employee
    template_name = "phonebook/phonebook.html"
    context_object_name = "employees"

    def get_queryset(self):
        return Employee.objects.filter(is_deleted=False).select_related("department__parent").order_by(
            "department__number", "name_ru", "name_kk"
        )


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = "phonebook/employee_detail.html"
    context_object_name = "employee"

    def get_queryset(self):
        return Employee.objects.filter(is_deleted=False)


class EmployeeAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Employee
    template_name = "phonebook/employee_form.html"
    fields = ["name_ru", "name_kk", "position_ru", "position_kk", "department", "email", "city_phone_number", "mobile_number", "photo"]
    success_url = reverse_lazy("phonebook")
    permission_required = "phonebook.add_employee"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EmployeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Employee
    template_name = "phonebook/employee_form.html"
    fields = ["name_ru", "name_kk", "position_ru", "position_kk", "department", "email", "city_phone_number", "mobile_number", "photo"]
    success_url = reverse_lazy("phonebook")
    permission_required = "phonebook.change_employee"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.POST.get("delete_photo_flag") == "1":
            self.object.delete_photo()
        return super().post(request, *args, **kwargs)


class EmployeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Employee
    template_name = "phonebook/employee_confirm_delete.html"
    success_url = reverse_lazy("phonebook")
    permission_required = "phonebook.delete_employee"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.deleted_by = request.user
        self.object.deleted_at = timezone.now()
        self.object.save()
        return redirect(self.success_url)


class HomePageView(TemplateView):
    template_name = "phonebook/index.html"
