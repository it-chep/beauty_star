from django import forms
from django.db import transaction

from main_site.models import Appointment, User, Worker


class CreateAppointmentForm(forms.Form):
    worker_id = forms.CharField(required=True, widget=forms.HiddenInput())
    service_id = forms.CharField(required=True, widget=forms.HiddenInput())
    period_id = forms.CharField(required=True, widget=forms.HiddenInput())

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-input__input', 'placeholder': 'Ваше имя'}
        ),
        required=True,
        label="Имя *",
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={'class': 'form-input__input', 'placeholder': 'Введите номер'}
        ),
        required=True,
        label="Телефон *",
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-input__input', 'placeholder': 'Введите email'}
        ),
        required=False,
        label="E-mail",
    )
    comment = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input__input', 'placeholder': 'Дополнительный комментарий'}),
        required=False,
        label="Ваши пожелания - дизайны, комментарии и тд",
    )

    notification_choice = forms.ChoiceField(
        choices=[],
        required=False,
        label="Напоминание",
    )

    def init_error_messages(self):
        self.fields['email'].error_messages.update({
            'invalid': 'Введите правильный адрес электронной почты.'
        })
        self.fields['name'].error_messages.update({
            'required': 'Это поле обязательно.'
        })
        self.fields['phone'].error_messages.update({
            'required': 'Это поле обязательно.'
        })

    def __init__(self, *args, **kwargs):
        super(CreateAppointmentForm, self).__init__(*args, **kwargs)

        self.fields['notification_choice'].choices = Appointment.NOTIFICATION_INTERVAL_CHOICES
        self.init_error_messages()

    def save(self):
        with transaction.atomic():
            user = User.objects.filter(username=self.cleaned_data['email']).first()
            if not user:
                user = User.objects.create(
                    username=self.cleaned_data['email'],
                    email=self.cleaned_data['email'],
                    first_name=self.cleaned_data['name'],
                    phone=self.cleaned_data['phone'],
                )

            appointment = Appointment.objects.create(
                schedule_period_id=self.cleaned_data['period_id'],
                user_id=user.id,
                draft=False,
                comment=self.cleaned_data['comment'],
                notification_choice=self.cleaned_data['notification_choice']
            )

        return appointment
