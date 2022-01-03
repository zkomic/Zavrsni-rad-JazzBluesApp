# Generated by Django 3.0 on 2021-08-16 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JazzBluesApp', '0018_auto_20210816_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 16, 14, 6, 44, 160239)),
        ),
        migrations.AlterField(
            model_name='event',
            name='ticket_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='eventorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 16, 14, 6, 44, 160239)),
        ),
    ]
