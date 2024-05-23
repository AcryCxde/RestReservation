# Generated by Django 5.0.6 on 2024-05-21 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_fireplace_image_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='booking',
            name='first_name',
            field=models.CharField(default='Иванов', max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='last_name',
            field=models.CharField(default='Иван', max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='phone_number',
            field=models.CharField(default='+7', max_length=20),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booked_time',
            field=models.CharField(choices=[('12:00-14:00', '12:00-14:00'), ('14:00-16:00', '14:00-16:00'), ('16:00-18:00', '16:00-18:00'), ('18:00-20:00', '18:00-20:00'), ('20:00-22:00', '20:00-22:00')], max_length=20),
        ),
        migrations.AlterField(
            model_name='fireplace',
            name='image_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
