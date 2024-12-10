from django.contrib.auth.models import Group

from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from main_site.models import (
    Appointment, Worker, ServiceSubGroup, Service, Schedule, ServiceGroup, SchedulePeriod, User, SiteSettings, Product
)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user',
        'schedule_period', 'status',
        'price', 'date_created',
        'draft',
    )

    raw_id_fields = [
        'user', 'schedule_period',
    ]


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('worker', 'service', 'date')

    raw_id_fields = [
        'worker', 'service',
    ]

    class SchedulePeriodAdminInline(admin.TabularInline):
        extra = 0
        model = SchedulePeriod

    inlines = [SchedulePeriodAdminInline]


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname')


class ServiceGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'subgroup', 'time_over')

    raw_id_fields = [
        'subgroup',
    ]


class ServiceSubGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_group')

    raw_id_fields = [
        'service_group',
    ]


class SchedulePeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'schedule')

    raw_id_fields = [
        'schedule',
    ]


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('id',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name', 'email', 'phone', 'tg_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(SchedulePeriod, SchedulePeriodAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(ServiceGroup, ServiceGroupAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceSubGroup, ServiceSubGroupAdmin)

admin.site.unregister(Group)

#  CELERY
PeriodicTask = apps.get_model('django_celery_beat', 'PeriodicTask')
CrontabSchedule = apps.get_model('django_celery_beat', 'CrontabSchedule')
IntervalSchedule = apps.get_model('django_celery_beat', 'IntervalSchedule')
SolarSchedule = apps.get_model('django_celery_beat', 'SolarSchedule')
ClockedSchedule = apps.get_model('django_celery_beat', 'ClockedSchedule')

admin.site.unregister(PeriodicTask)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
#  CELERY
