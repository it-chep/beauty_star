import locale
from datetime import datetime
from urllib.parse import urlencode

from django.db.models import Count
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect

import logging

from django.urls import reverse
from django.views.generic import TemplateView

from main_site.forms import CreateAppointmentForm
from main_site.models import Worker, Service, SchedulePeriod, User, Appointment, Product, ServiceGroup
from main_site.utils import get_site_url
from main_site.bot_handler import bot

logger = logging.getLogger(__name__)


class OnlineBookingView(TemplateView):
    http_method_names = ["get"]

    template_name = "beauty_star/online_booking.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class CreateAppointmentView(TemplateView):
    http_method_names = ["get", "post"]

    template_name = "beauty_star/create_appointment.html"

    form_class = CreateAppointmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker_id = self.request.GET.get('worker_id')
        service_id = self.request.GET.get('service_id')
        period_id = self.request.GET.get('period_id')

        try:
            unique_service_groups = set()
            if int(worker_id) == -1:
                worker = Worker.objects.filter(services__id=service_id).order_by('?').prefetch_related(
                    'services', 'services__subgroup', 'services__subgroup__service_group'
                ).first()
            else:
                worker = Worker.objects.filter(id=worker_id).prefetch_related(
                    'services', 'services__subgroup', 'services__subgroup__service_group'
                ).first()

            if not worker:
                # todo 404
                raise Http404

        except Worker.DoesNotExist:
            return

        if not worker or not service_id or not period_id:
            return

        form = self.form_class(
            initial={'worker_id': worker_id, 'service_id': service_id, 'period_id': period_id}
        )

        context['form'] = form
        context['worker'] = worker
        context['services'] = Service.objects.filter(id=service_id)
        period = SchedulePeriod.objects.filter(id=period_id).select_related('schedule').first()
        if period:
            locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
            current_year = datetime.now().year
            schedule_date = period.schedule.date
            formatted_date = schedule_date.strftime('%d %B')

            if schedule_date.year != current_year:
                formatted_date += f' {schedule_date.year}'

            context['date'] = formatted_date
            context['time'] = f"{period.date_time_start.strftime('%H:%M')}"
        return context

    def get_notification_text(self):
        worker_id = self.request.POST.get('worker_id')
        service_id = self.request.POST.get('service_id')
        period_id = self.request.POST.get('period_id')
        phone = self.request.POST.get('phone')
        email = self.request.POST.get('email')
        client_name = self.request.POST.get('name')
        notification_text = \
            Appointment.NOTIFICATION_INTERVAL_CHOICES[int(self.request.POST.get('notification_choice'))][1]
        comment = self.request.POST.get('comment')

        if not comment:
            comment = "Отсутствует"

        period = SchedulePeriod.objects.select_related('schedule').get(id=period_id)

        text = (
            f'Новая запись на услугу!\n\nИмя клиента: {client_name}\n\nУслуга:\n"{Service.objects.get(id=service_id).name}"\n\n '
            f'Мастер:\n"{Worker.objects.get(id=worker_id).full_name}" \n\nДата и время:\n\n{period.schedule.date.strftime("%d.%m.%Y")}\n{period.date_time_start}\n\n'
            f'Связаться можно по телефону {phone} или по email {email}. \n\nПользователь попросил напомнить ему о записи: \n{notification_text}\n\n'
            f'Дополнительный комментарий:\n{comment}'
        )

        return text

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        result = {"success": False}

        if form.is_valid():
            appointment = form.save()

            params = {"appointment_id": appointment.id}
            query_string = urlencode(params)

            redirect_url = f"{get_site_url()}{reverse('spasibochki')}?{query_string}"
            result.update({"success": True, "redirect_url": redirect_url})
            admin = User.objects.filter(is_superuser=True).exclude(tg_id__isnull=True).first()
            if admin:
                bot.send_message(admin.tg_id, self.get_notification_text())
        else:
            result.update({"errors": form.errors})

        return JsonResponse(result)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not context:
            return redirect('homepage')
        return render(request, self.template_name, context)


class GetWorkersView(TemplateView):
    http_method_names = ["get"]

    template_name = "beauty_star/get_workers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        period_id = self.request.GET.get('period_id')
        service_id = self.request.GET.get('service_id')

        if period_id and service_id:
            workers = Worker.objects.filter(
                schedules__periods__id=period_id,
                services__id=service_id
            ).distinct()
            context["action_url"] = get_site_url() + reverse('create_appointment')
            context["back_url"] = get_site_url() + reverse('online_booking')
            context["action_text"] = 'Готово'
        elif not service_id:
            workers = Worker.objects.filter(
                schedules__periods__id=period_id,
            ).distinct()
            context["action_url"] = get_site_url() + reverse('get_service')
            context["back_url"] = get_site_url() + reverse('online_booking')
            context["action_text"] = 'Выберите услугу'
        elif not period_id:
            workers = Worker.objects.filter(
                services__id=service_id
            ).distinct()
            context["action_url"] = get_site_url() + reverse('get_time')
            context["back_url"] = get_site_url() + reverse('get_service')
            context["action_text"] = 'Выберите дату и время'

        if not service_id and not period_id:
            workers = Worker.objects.all().prefetch_related(
                'services', 'services__subgroup', 'services__subgroup__service_group'
            ).order_by('id')

        context["workers"] = workers

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class GetServiceView(TemplateView):
    http_method_names = ["get"]

    template_name = "beauty_star/get_service.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker_id = self.request.GET.get('worker_id')

        if worker_id:
            try:
                worker_id = int(worker_id)
            except TypeError:
                return None
        workers = Worker.objects.all()
        period_id = self.request.GET.get('period_id')
        if period_id and worker_id:
            context["action_url"] = get_site_url() + reverse('create_appointment')
            context["back_url"] = get_site_url() + reverse('online_booking')
            context["action_text"] = 'Готово'
        elif not worker_id:
            context["action_url"] = get_site_url() + reverse('get_worker')
            context["back_url"] = get_site_url() + reverse('online_booking')
            context["action_text"] = 'Выберите специалиста'
        elif not period_id:
            context["action_url"] = get_site_url() + reverse('get_time')
            context["back_url"] = get_site_url() + reverse('get_worker')
            context["action_text"] = 'Выберите дату и время'

        services_by_group = {}

        if worker_id == -1 or not worker_id and not period_id:
            services = Service.objects.annotate(num_workers=Count('worker')).filter(num_workers__gt=0)
        elif worker_id == -1 or not worker_id and period_id:
            workers = Worker.objects.filter(
                schedules__periods__id=period_id,
            )
            services = set()
            for worker in workers:
                for service in worker.services.all():
                    services.add(service)
        else:
            worker = workers.filter(id=worker_id).prefetch_related('services').first()
            if worker:
                services = worker.services.all()
                context['worker'] = worker
            else:
                services = []

        # Группируем услуги по группам и подгруппам
        for service in services:
            group = service.subgroup.service_group
            if group not in services_by_group:
                services_by_group[group] = {}
            if service.subgroup not in services_by_group[group]:
                services_by_group[group][service.subgroup] = []
            services_by_group[group][service.subgroup].append(service)

        context['services_by_group'] = services_by_group

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class GetTimeView(TemplateView):
    http_method_names = ["get"]

    template_name = "beauty_star/get_time.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker_id = self.request.GET.get('worker_id')
        service_id = self.request.GET.get('service_id')
        if worker_id and service_id:
            context["action_url"] = get_site_url() + reverse('create_appointment')
            context["back_url"] = get_site_url() + reverse('online_booking')
            context["action_text"] = 'Готово'
        elif not service_id:
            context["action_url"] = get_site_url() + reverse('get_service')
            context["back_url"] = get_site_url() + reverse('online_booking')
            context["action_text"] = 'Выберите услугу'
        elif not worker_id:
            context["action_url"] = get_site_url() + reverse('get_worker')
            context["back_url"] = get_site_url() + reverse('get_service')
            context["action_text"] = 'Выберите специалиста'

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class WorkerDetailView(TemplateView):
    http_method_names = ["get"]

    template_name = "beauty_star/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker_id = kwargs.get('worker_id')
        worker = Worker.objects.prefetch_related(
            'services', 'services__subgroup', 'services__subgroup__service_group'
        ).get(id=worker_id)
        context['worker'] = worker
        context['services'] = worker.services.all()

        period_id = self.request.GET.get('period_id')
        service_id = self.request.GET.get('service_id')
        context["action_text"] = 'Выбрать специалиста'

        if period_id and service_id:
            context["action_url"] = get_site_url() + reverse('create_appointment')
            context["action_text"] = 'Готово'
        elif not service_id:
            context["action_url"] = get_site_url() + reverse('get_service')
        elif not period_id:
            context["action_url"] = get_site_url() + reverse('get_time')

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class SpasiboView(TemplateView):
    http_method_names = ["get"]

    template_name = "beauty_star/spasibochki.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = Appointment.objects.filter(id=self.request.GET.get('appointment_id')).select_related(
            'schedule_period__schedule__worker', 'schedule_period__schedule__service',
        ).first()
        if appointment:
            context["appointment"] = appointment
        else:
            raise Http404

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class HomePageView(TemplateView):
    http_method_names = ["get"]

    template_name = "beauty_star/main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_groups"] = ServiceGroup.objects.prefetch_related(
            'subgroups__services', 'subgroups',
        )
        context["workers"] = Worker.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class CatalogView(TemplateView):
    http_method_names = ["get"]
    template_name = "beauty_star/catalog.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {"products": products}
        return render(request, self.template_name, context)


def page_400(request, exception):
    return render(request, 'beauty_star/error_page.html', status=404)


def page_500(request):
    return render(request, 'beauty_star/error_page.html', status=500)
