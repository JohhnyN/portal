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
from .models import Department, Employee


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name_ru', 'name_kk', 'type', 'parent']


class DepartmentListView(ListView):
    model = Department
    template_name = "phonebook/department_list.html"
    context_object_name = "departments"


class DepartmentDetailView(DetailView):
    model = Department
    template_name = "phonebook/department_detail.html"
    context_object_name = "department"


class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Department
    template_name = "phonebook/department_form.html"
    fields = ["name_ru", "name_kk", "type", "parent"]
    success_url = reverse_lazy("department_list")
    permission_required = "phonebook.add_department"


class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Department
    template_name = "phonebook/department_form.html"
    fields = ["name_ru", "name_kk", "type", "parent"]
    success_url = reverse_lazy("department_list")
    permission_required = "phonebook.change_department"


class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Department
    template_name = "phonebook/department_confirm_delete.html"
    success_url = reverse_lazy("department_list")
    permission_required = "phonebook.delete_department"


class EmployeeListView(ListView):
    model = Employee
    template_name = "phonebook/phonebook.html"
    context_object_name = "employees"

    def get_queryset(self):
        return Employee.objects.select_related("department__parent").order_by(
            "department__number", "name_ru", "name_kk"
        )


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = "phonebook/employee_detail.html"
    context_object_name = "employee"


class EmployeeAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Employee
    template_name = "phonebook/employee_form.html"
    fields = "__all__"
    success_url = reverse_lazy("phonebook")
    permission_required = "phonebook.add_employee"


class EmployeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Employee
    template_name = "phonebook/employee_form.html"
    fields = "__all__"
    success_url = reverse_lazy("phonebook")
    permission_required = "phonebook.change_employee"

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


class HomePageView(TemplateView):
    template_name = "phonebook/index.html"
