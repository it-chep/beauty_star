import os
import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import UniqueConstraint

APP_MEDIA_DIR = "beauty_star"

PHONE_VALIDATOR = RegexValidator(
    regex=r"[0-9( )\-+]{6,20}", message="Телефон должен состоять из цифр +-(). Введите корректный номер телефона."
)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    tg_id = models.BigIntegerField(verbose_name="TG ID", blank=True, null=True)
    phone = models.CharField(
        max_length=30, validators=[RegexValidator(
            regex='[0-9( )\\-+]{6,20}',
            message='Телефон должен состоять из цифр +-(). Введите корректный номер телефона.'
        )], default="", blank=True, null=True, verbose_name="Номер телефона"
    )
    first_name = models.CharField("Имя", default="", max_length=255, blank=True, null=True)
    last_name = models.CharField("Фамилия", default="", max_length=255, blank=True, null=True)
    middle_name = models.CharField("Отчество", default="", max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.username


class Appointment(models.Model):
    APPOINTMENT_STATUS_CHOICES = (
        (1, 'Новый'),
        (2, 'Не состоялся'),
        (3, 'Отменен'),
        (4, 'Завершен')
    )

    NOTIFICATION_INTERVAL_CHOICES = (
        (0, 'Не напоминать'),
        (1, 'За 1 час'),
        (2, 'За 2 часа'),
        (3, 'За 3 часа'),
        (4, 'За 4 часа'),
        (5, 'За 6 часов'),
        (6, 'За 24 часа'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Клиент",
        null=True,
        blank=True,
        related_name="appointments"
    )

    schedule_period = models.ForeignKey(
        "SchedulePeriod",
        verbose_name="Календарный слот",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments"
    )

    status = models.SmallIntegerField(
        verbose_name="Статус",
        choices=APPOINTMENT_STATUS_CHOICES,
        default=1
    )

    comment = models.TextField(verbose_name="Комментарий клиента")
    notification_choice = models.SmallIntegerField(
        verbose_name="Напоминание",
        choices=NOTIFICATION_INTERVAL_CHOICES,
        default=0,
    )

    price = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name="Стоимость от",
        null=True,
        blank=True,
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания",
    )

    draft = models.BooleanField(
        verbose_name="Черновик",
        default=True,
    )

    is_notificated = models.BooleanField(
        default=False,
        verbose_name="Напоминание отправлено",
    )

    admin_hotificate_user = models.BooleanField(
        default=False,
        verbose_name="Админ напомнил о записи",
    )

    class Meta:
        verbose_name = "Онлайн-запись"
        verbose_name_plural = "Онлайн-записи"

    def __str__(self):
        return f"Онлайн-запись на {self.schedule_period.schedule.date}: {self.schedule_period.date_time_start}"


class Service(models.Model):
    name = models.CharField(
        verbose_name="Название услуги",
        max_length=255,
    )

    price = models.DecimalField(
        verbose_name="Цена от",
        max_digits=16,
        decimal_places=2,
        default=0
    )

    subgroup = models.ForeignKey(
        "ServiceSubGroup",
        on_delete=models.SET_NULL,
        related_name="services",
        null=True
    )

    time_over = models.IntegerField(
        verbose_name="Количество времени (в минутах)",
        default=30,
    )

    # description = models.TextField(
    #     verbose_name="Описание услуги"
    # )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class ServiceGroup(models.Model):
    name = models.CharField(
        verbose_name="Название группы услуг",
        max_length=255,
    )

    class Meta:
        verbose_name = "Группа услуг"
        verbose_name_plural = "Группы услуг"

    def __str__(self):
        return self.name

    @property
    def has_services(self):
        return any(subgroup.services.exists() for subgroup in self.subgroups.all())


class ServiceSubGroup(models.Model):
    name = models.CharField(
        verbose_name="Название подгруппы услуг",
        max_length=255,
    )

    service_group = models.ForeignKey(
        "ServiceGroup",
        verbose_name="Группа услуг",
        on_delete=models.CASCADE,
        related_name="subgroups",
    )

    class Meta:
        verbose_name = "Подгруппа услуг"
        verbose_name_plural = "Подгруппы услуг"

    def __str__(self):
        return self.name


class Schedule(models.Model):
    worker = models.ForeignKey(
        'Worker',
        on_delete=models.CASCADE,
        verbose_name="Специалист",
        related_name="schedules",
    )

    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        verbose_name="Услуга",
        related_name="schedules"
    )

    date = models.DateField(
        verbose_name="Дата начала"
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['worker', 'service', 'date'], name='unique_worker_service_date')
        ]
        verbose_name = "Календарь"
        verbose_name_plural = "Календари"

    def __str__(self):
        return f"{self.service.name} {self.date}"


class SchedulePeriod(models.Model):
    schedule = models.ForeignKey(
        "Schedule",
        on_delete=models.CASCADE,
        verbose_name="Календарь",
        related_name="periods",
    )

    date_time_start = models.TimeField(
        verbose_name="Время начала"
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['schedule', 'date_time_start'], name='unique_schedule_period')
        ]
        verbose_name = "Календарный слот"
        verbose_name_plural = "Календарные слоты"

    def __str__(self):
        return f"{self.schedule.service.name} {self.schedule.date}: {self.date_time_start}"


def upload_to_worker_photo(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(APP_MEDIA_DIR, instance.BASE_UPLOAD_DIR, filename)


class Worker(models.Model):
    BASE_UPLOAD_DIR = "workers_photos"

    name = models.CharField(
        verbose_name="Имя специалиста",
        max_length=255
    )
    surname = models.CharField(
        verbose_name="Фамилия специалиста",
        max_length=255
    )
    services = models.ManyToManyField(
        "Service",
        verbose_name="Услуги специалиста",
    )

    photo = models.ImageField(
        verbose_name="Фото",
        upload_to=upload_to_worker_photo
    )

    job_title = models.CharField(
        verbose_name="Должность сотрудника (Вводится в ручную)",
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"

    def __str__(self):
        return f"{self.name} {self.surname}"

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"

    @property
    def service_group_display(self):
        unique_service_groups = set()
        for service in self.services.all():
            if service.subgroup and service.subgroup.service_group:
                unique_service_groups.add(service.subgroup.service_group.name)
        return str(', '.join(unique_service_groups))


class SiteSettings(models.Model):
    BASE_UPLOAD_DIR = "site_content"
    favicon = models.ImageField(
        upload_to=upload_to_worker_photo,
        null=True,
        blank=True
    )

    logo = models.ImageField(
        upload_to=upload_to_worker_photo,
        null=True,
        blank=True
    )

    homepage_cell_1 = models.ForeignKey(
        to='Service',
        related_name="homepage_cell_1",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    homepage_cell_2 = models.ForeignKey(
        to='Service',
        related_name="homepage_cell_2",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    homepage_cell_3 = models.ForeignKey(
        to='Service',
        related_name="homepage_cell_3",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    homepage_cell_4 = models.ForeignKey(
        to='Service',
        related_name="homepage_cell_4",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    homepage_cell_5 = models.ForeignKey(
        to='Service',
        related_name='homepage_cell_5',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    homepage_cell_6 = models.ForeignKey(
        to='Service',
        related_name="homepage_cell_6",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    telegram_url = models.URLField(
        verbose_name="Ссылка на телеграм",
        null=True,
        blank=True,
    )

    youtube_url = models.URLField(
        verbose_name="Ссылка на YouTube",
        null=True,
        blank=True,
    )

    instagram_url = models.URLField(
        verbose_name="Ссылка на Instagram",
        null=True,
        blank=True,
    )

    whatsapp_url = models.URLField(
        verbose_name="Ссылка на Whatsapp",
        null=True,
        blank=True,
    )

    support_phone = models.CharField(
        verbose_name="Телефон обратной связи",
        null=True,
        blank=True,
    )

    support_email = models.EmailField(
        verbose_name="Email обратной связи",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Настройка сайта"
        verbose_name_plural = "Настройки сайта"


class Product(models.Model):
    BASE_UPLOAD_DIR = "product_photos"

    photo = models.ImageField(upload_to=upload_to_worker_photo)
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание товара", blank=True, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Цена за штуку", null=True, blank=True)
    ordering_number = models.IntegerField(verbose_name="Порядок сортировки", null=True, blank=True)

    class Meta:
        verbose_name = "Товар с витрины"
        verbose_name_plural = "Товары с витрины"
