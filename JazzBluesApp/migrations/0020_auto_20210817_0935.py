# Generated by Django 3.0 on 2021-08-17 07:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JazzBluesApp', '0019_auto_20210816_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 9, 35, 2, 890200)),
        ),
        migrations.AlterField(
            model_name='eventorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 9, 35, 2, 890200)),
        ),
    ]
