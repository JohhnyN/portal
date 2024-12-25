from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import (
    DepartmentListView,
    DepartmentDetailView,
    EmployeeDetailView,
    DepartmentCreateView,
    DepartmentUpdateView,
    DepartmentDeleteView,
    EmployeeAddView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    HomePageView,
    EmployeeListView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('phonebook/', EmployeeListView.as_view(), name="phonebook"),
    path('departments/', DepartmentListView.as_view(), name="department_list"),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name="department_detail"),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name="employee_detail"),
    path('departments/add/', DepartmentCreateView.as_view(), name="department_add"),
    path('departments/update/<int:pk>/', DepartmentUpdateView.as_view(), name="department_update"),
    path('departments/delete/<int:pk>/', DepartmentDeleteView.as_view(), name="department_delete"),
    path('employees/add/', EmployeeAddView.as_view(), name="employee_add"),
    path('employees/update/<int:pk>/', EmployeeUpdateView.as_view(), name="employee_update"),
    path('employees/delete/<int:pk>/', EmployeeDeleteView.as_view(), name="employee_delete"),
    path('login/', auth_views.LoginView.as_view(template_name="phonebook/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
