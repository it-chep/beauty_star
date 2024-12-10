from django.conf import settings
from django.conf.urls import include

from django.urls import path, reverse_lazy

from main_site.bot_handler import telegram_webhook
from main_site.views import (
    OnlineBookingView,
    CreateAppointmentView,
    HomePageView,
    GetWorkersView,
    WorkerDetailView,
    GetServiceView,
    GetTimeView,
    SpasiboView,
    CatalogView,
)

urlpatterns = [
    path('api/v1/', include('main_site.api.urls')),
    path('online_booking/', OnlineBookingView.as_view(), name='online_booking'),
    path('create_appointment/', CreateAppointmentView.as_view(), name='create_appointment'),
    path('get_worker/', GetWorkersView.as_view(), name='get_worker'),
    path('worker_info/<int:worker_id>/', WorkerDetailView.as_view(), name='worker_info'),
    path('get_time/', GetTimeView.as_view(), name='get_time'),
    path('get_service/', GetServiceView.as_view(), name='get_service'),
    path('spasibochki/', SpasiboView.as_view(), name='spasibochki'),
    path('address/', OnlineBookingView.as_view(), name='address'),
    path('services/', OnlineBookingView.as_view(), name='services'),
    path('prices/', OnlineBookingView.as_view(), name='prices'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path(f'{settings.BOT_TOKEN}/', telegram_webhook, name='bot'),

    path('', HomePageView.as_view(), name='homepage')
]
