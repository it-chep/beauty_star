import logging
from datetime import timedelta, datetime

from django.urls import reverse

from main_site.bot_handler import bot
from main_site.celery import app
from main_site.models import Appointment, User
from main_site.utils import get_site_url

logger = logging.getLogger("default")


@app.task
def check_appointment_notification():
    appointments = Appointment.objects.filter(
        status=1,
        is_notificated=False,
    ).select_related('schedule_period').exclude(notification_choice=0)

    admin = User.objects.filter(is_superuser=True).exclude(tg_id__isnull=True).first()
    now = datetime.now()
    for appointment in appointments:
        redirect_url = f"{get_site_url()}{reverse('admin:main_site_appointment_change', args=[appointment.id])}"
        message_text = (
            f'Напоминаю, необходимо связаться с клиентом "{appointment.user.first_name.strip()} {appointment.user.last_name.strip()}".\n\n'
            f'Он просил напомнить ему о записи {Appointment.NOTIFICATION_INTERVAL_CHOICES[appointment.notification_choice][1]}.\n\n'
            f'Связаться с ним можно по телефону {appointment.user.phone.strip()} или через почту {appointment.user.email}.\n\n'
            f'Детальную информацию о записи можно посмотреть \n{redirect_url}'
        )

        start_datetime = datetime.combine(appointment.schedule_period.schedule.date, appointment.schedule_period.date_time_start)
        if appointment.notification_choice == 1 and start_datetime <= now - timedelta(hours=1):
            bot.send_message(admin.tg_id, message_text)
            appointment.is_notificated = True
            appointment.save()
        elif appointment.notification_choice == 2 and now - timedelta(hours=2) <= start_datetime <= now - timedelta(hours=1):
            bot.send_message(admin.tg_id, message_text)
            appointment.is_notificated = True
            appointment.save()
        elif appointment.notification_choice == 3 and now - timedelta(hours=2) <= start_datetime <= now + timedelta(hours=3):
            bot.send_message(admin.tg_id, message_text)
            appointment.is_notificated = True
            appointment.save()
        elif appointment.notification_choice == 4 and now + timedelta(hours=3) <= start_datetime <= now + timedelta(hours=4):
            bot.send_message(admin.tg_id, message_text)
            appointment.is_notificated = True
            appointment.save()
        elif appointment.notification_choice == 5 and now + timedelta(hours=4) <= start_datetime <= now + timedelta(hours=5):
            bot.send_message(admin.tg_id, message_text)
            appointment.is_notificated = True
            appointment.save()
        elif appointment.notification_choice == 6 and now + timedelta(hours=18) <= start_datetime <= now + timedelta(days=1):
            bot.send_message(admin.tg_id, message_text)
            appointment.is_notificated = True
            appointment.save()
