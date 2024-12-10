from django.urls import path
from main_site.api.views import ChooseTimeApiView

urlpatterns = [
    path('choose_time/', ChooseTimeApiView.as_view(), name='choose_time'),
]