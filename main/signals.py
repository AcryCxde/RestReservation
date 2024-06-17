from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import telegram
import asyncio

# Telegram bot settings
TELEGRAM_BOT_TOKEN = '7311775466:AAGw5TOsjMyIcNnEpOh8xQzyaOSlsX9ZRaU'
TELEGRAM_CHAT_ID = '440854538'


@receiver(post_save, sender=Booking)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        # Отправка уведомления о новом бронировании в Telegram
        asyncio.run(send_telegram_message(instance))

    if instance.is_verified and not created:
        # Отправка подтверждения бронирования по email
        subject = 'Подтверждение бронирования'
        html_message = render_to_string('success_mail_template.html', {'booking': instance})
        plain_message = strip_tags(html_message)
        recipient_list = [instance.email]
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, recipient_list, False, html_message=html_message)


async def send_telegram_message(instance):
    message = (f'Новое бронирование:\n\n'
               f'Костровое место: {instance.fireplace.name}\n'
               f'Дата: {instance.booking_date}\n'
               f'Время: {instance.booked_time}\n'
               f'Имя: {instance.first_name} {instance.last_name}\n'
               f'Телефон: {instance.phone_number}\n'
               f'Email: {instance.email}\n'
               f'Проверьте оплату и подтвердите бронирование в административной панели.')
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)