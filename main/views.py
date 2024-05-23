from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Booking, FirePlace
from datetime import *


all_time_slots = [
        '12:00-14:00',
        '14:00-16:00',
        '16:00-18:00',
        '18:00-20:00',
        '20:00-22:00',
    ]
def index(request):
    return render(request,'index.html')

def PickDay(request):
    return render(request,'Pick_day.html')

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


    if not id_str or int(id_str) < 1 or int(id_str) > 4:
        return redirect('exception')
    fireplace = FirePlace.objects.get(id=int(id_str))
    print(fireplace)

    if date_str:
        try:
            picked_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            # Если дата в неверном формате, установить сегодняшнюю дату
            return redirect('exception')
    else:
        return redirect('exception')

    min_date = date.today()
    max_date = date(2024, 8, 31)

    if picked_date < min_date or picked_date > max_date:
        return redirect('exception')

    if time_str not in all_time_slots:
        return redirect('exception')

    context = {
        'picked_date': picked_date,
        'time_str': time_str,
        'fireplace': fireplace,
    }
    return render(request,'booking_form.html', context)


def exception(request):
    return render(request, 'exception.html')


