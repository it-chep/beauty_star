from django.db.models import OuterRef, Subquery
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from main_site.models import SchedulePeriod, Appointment


class ChooseTimeApiView(APIView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs) -> Response:
        date = request.GET.get("date")
        service_id = request.GET.get("service_id")
        worker_id = request.GET.get("worker_id")
        exclude_times = Appointment.objects.filter(
            schedule_period__schedule__date=date
        ).values('schedule_period__date_time_start')

        periods = SchedulePeriod.objects.filter(
            schedule__date=date
        ).exclude(
            date_time_start__in=Subquery(exclude_times)
        ).order_by('date_time_start')

        try:
            if worker_id:
                worker_id = int(worker_id)
            if service_id:
                service_id = int(service_id)
        except TypeError:
            raise Http404

        if worker_id and worker_id > 0:
            periods.filter(worker_id=worker_id)
        if service_id and service_id > 0:
            periods.filter(schedule__service__id=service_id)

        periods_display = []

        for period in periods:
            periods_display.append({
                "id": period.id,
                'date_time_start': period.date_time_start.strftime("%H:%M"),
            })

        data = {'schedule_periods': periods_display}

        return Response(
            data=data,
            status=200,
        )
