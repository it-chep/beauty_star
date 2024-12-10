import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

bot = telebot.TeleBot(settings.BOT_TOKEN)


#
# def set_bot_webhook():
#     bot.set_webhook(f'{settings.WEBHOOK_URL}/{settings.BOT_TOKEN}/')
#
#
# set_bot_webhook()


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])
    return HttpResponse(status=200)


START_MESSAGE = "Привет я создан для уведомлений"


class Handler:
    bot = bot

    @staticmethod
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, START_MESSAGE)
