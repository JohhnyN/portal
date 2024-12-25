from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

class Department(MPTTModel):
    ORGANIZATION = "ORGANIZATION"
    DEPARTMENT = "DEPARTMENT"
    DIVISION = "DIVISION"

    type_choices = [
        (ORGANIZATION, _("Организация")),
        (DEPARTMENT, _("Департамент")),
        (DIVISION, _("Отдел")),
    ]

    name_ru = models.CharField(max_length=120, verbose_name=_("Название на русском"))
    name_kk = models.CharField(max_length=120, verbose_name=_("Название на казахском"))

    type = models.CharField(
        choices=type_choices,
        max_length=50,
        help_text=_("Тип подразделения"),
        verbose_name=_("Тип подразделения"),
    )

    number = models.PositiveIntegerField(
        help_text=_("Порядковый номер для вывода на сайт"),
        verbose_name=_("Порядковый номер для вывода на сайт"),
        default=0
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        help_text=_("Родительское подразделение"),
        verbose_name=_("Родительское подразделение"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Дата обновления"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_departments",
        verbose_name=_("Создано пользователем"),
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_departments",
        verbose_name=_("Обновлено пользователем"),
    )

    class MPTTMeta:
        order_insertion_by = ["name_ru"]

    class Meta:
        verbose_name = _("Подразделение")
        verbose_name_plural = _("Подразделения")

    def __str__(self):
        return f"{self.get_type_display()}: {self.name_ru}"

class CityPhoneNumber(models.Model):
    number = models.CharField(max_length=20, verbose_name=_("Городской номер телефона"))    

    class Meta:
        verbose_name = _("Городской номер телефона")
        verbose_name_plural = _("Городские номера телефонов")

    def __str__(self):
        return self.number

class Employee(models.Model):
    name_ru = models.CharField(max_length=300, verbose_name=_("ФИО на русском"))
    name_kk = models.CharField(max_length=300, verbose_name=_("ФИО на казахском"))
    position_ru = models.CharField(max_length=100, verbose_name=_("Должность на русском"))
    position_kk = models.CharField(max_length=100, verbose_name=_("Должность на казахском"))
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name=_("Подразделение"),
    )
    email = models.EmailField(
        verbose_name=_("Email"), blank=True, null=True
    )
    city_phone_number = models.ForeignKey(
        CityPhoneNumber,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
        verbose_name=_("Городской номер телефона"),
    )
    mobile_number = models.CharField(
        max_length=20, verbose_name=_("Сотовый номер"), blank=True, null=True
    )
    photo = models.ImageField(
        upload_to="photos/", blank=True, null=True, verbose_name=_("Фото")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Дата обновления"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_employees",
        verbose_name=_("Создано пользователем"),
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_employees",
        verbose_name=_("Обновлено пользователем"),
    )

    class Meta:
        verbose_name = _("Сотрудник")
        verbose_name_plural = _("Сотрудники")

    def __str__(self):
        return self.name_ru

@receiver(pre_save, sender=Employee)
def set_updated_at(sender, instance, **kwargs):
    if instance.pk:
        instance.updated_at = timezone.now()

@receiver(pre_save, sender=Department)
def set_department_updated_at(sender, instance, **kwargs):
    if instance.pk:
        instance.updated_at = timezone.now()
