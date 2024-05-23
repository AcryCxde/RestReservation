from django.db import models
from django.core.exceptions import ValidationError


class FirePlace(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    cost = models.IntegerField(blank=False, null=False)
    image_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    TIME_SLOTS = [
        ('12:00-14:00', '12:00-14:00'),
        ('14:00-16:00', '14:00-16:00'),
        ('16:00-18:00', '16:00-18:00'),
        ('18:00-20:00', '18:00-20:00'),
        ('20:00-22:00', '20:00-22:00'),
    ]

    fireplace = models.ForeignKey(FirePlace, related_name='bookings', on_delete=models.CASCADE)
    booked_time = models.CharField(max_length=20, choices=TIME_SLOTS, blank=False, null=False)
    booking_date = models.DateField(blank=False, null=False, default='2000-01-01')
    first_name = models.CharField(max_length=100, blank=False, null=False, default='Иванов')
    last_name = models.CharField(max_length=100, blank=False, null=False, default='Иван')
    phone_number = models.CharField(max_length=20, blank=False, null=False, default='+7')

    def clean(self):
        # Проверка на наличие брони в тот же день и временной слот
        if Booking.objects.filter(fireplace=self.fireplace, booking_date=self.booking_date,
                                  booked_time=self.booked_time).exists():
            raise ValidationError('Этот слот уже занят на текущую дату')

    def __str__(self):
        return f'{self.fireplace.name} - {self.booking_date} {self.booked_time}'

