# Generated by Django 3.0 on 2021-08-17 09:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JazzBluesApp', '0025_auto_20210817_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 11, 14, 30, 81659)),
        ),
        migrations.AlterField(
            model_name='eventorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 11, 14, 30, 81659)),
        ),
    ]
