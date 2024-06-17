import requests
from django.db.models import Min, Max
from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Booking, FirePlace
from datetime import *
from jsonrpcserver import method, dispatch
from datetime import datetime, date
from django.http import JsonResponse
from django.conf import settings
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

all_time_slots = [
        '12:00-14:00',
        '14:00-16:00',
        '16:00-18:00',
        '18:00-20:00',
        '20:00-22:00',
    ]


def check_bookings(request):
    date_str = request.GET.get('date')

    if date_str:
        try:
            picked_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            # Если дата в неверном формате, установить сегодняшнюю дату
            return redirect('exception')
    else:
        return redirect('exception')

    # Проверка диапазона дат
    min_date = date.today()
    max_date = date(2024, 8, 31)

    if picked_date < min_date or picked_date > max_date:
        return redirect('exception')

    bookings = Booking.objects.filter(booking_date=picked_date) if picked_date else []

    fireplaces = FirePlace.objects.all()

    booked_slots = {}
    for fireplace in fireplaces:
        booked_slots[fireplace.id] = list(
            bookings.filter(fireplace=fireplace).values_list('booked_time', flat=True)
        )

    context = {
        'picked_date': picked_date,
        'fireplaces': fireplaces,
        'booked_slots': booked_slots,
        'all_time_slots': all_time_slots,
    }

    return render(request, 'check_bookings.html', context)

def booking_form(request):
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')
    id_str = request.GET.get('id')

    fireplace_ids = FirePlace.objects.aggregate(min_id=Min('id'), max_id=Max('id'))
    first_fireplace_id = fireplace_ids['min_id']
    last_fireplace_id = fireplace_ids['max_id']

    if not id_str or int(id_str) < first_fireplace_id or int(id_str) > last_fireplace_id:
        return redirect('exception')

    fireplace = FirePlace.objects.get(id=int(id_str))

    if date_str:
        try:
            picked_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return redirect('exception')
    else:
        return redirect('exception')

    min_date = date.today()
    max_date = date(2024, 8, 31)

    if picked_date < min_date or picked_date > max_date:
        return redirect('exception')

    if time_str not in all_time_slots:
        return redirect('exception')

    if request.method == 'POST':
        name = request.POST.get('name')
        if len(name.split()) <= 1:
            first_name = name
            last_name = ''
        else:
            first_name = name.split()[0]
            last_name = name.split()[1]
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # Verify reCAPTCHA
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']:
            booking_data = [
                fireplace,
                time_str,
                picked_date,
                first_name,
                last_name,
                phone,
                email,
                False,
                fireplace.cost
            ]
            if make_booking(booking_data):
                return redirect('booked')
            else:
                return redirect('exception')
        else:
            context = {
                'picked_date': picked_date,
                'time_str': time_str,
                'fireplace': fireplace,
                'public_key': settings.RECAPTCHA_PUBLIC_KEY,
                'error_message': 'Вы не прошли reCAPTCHA. Пожалуйста попробуйте ещё раз.'
            }
            return render(request, 'booking_form.html', context)

    context = {
        'picked_date': picked_date,
        'time_str': time_str,
        'fireplace': fireplace,
        'public_key': settings.RECAPTCHA_PUBLIC_KEY
    }
    return render(request, 'booking_form.html', context)

def make_booking(data):
    booking = Booking(
        fireplace=data[0],
        booked_time=data[1],
        booking_date=data[2],
        first_name=data[3],
        last_name=data[4],
        phone_number=data[5],
        email=data[6],
        is_verified=data[7]
    )
    if booking.isUnik():
        booking.save()
    else:
        return False

    subject = f'Бронь кострового места на {data[1]} {data[2]}'
    html_message = render_to_string('mail_template.html', {'data': data})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [data[6]], False, html_message=html_message)
    return True

async def booked(request):
    return render(request,'booked.html')
async def index(request):
    return render(request,'index.html')
async def PickDay(request):
    return render(request,'Pick_day.html')
async def exception(request):
    return render(request, 'exception.html')


