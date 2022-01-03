# Generated by Django 3.0 on 2021-08-17 07:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JazzBluesApp', '0020_auto_20210817_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='number_of_tickets',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='in_stock',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='albumorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 9, 48, 11, 395421)),
        ),
        migrations.AlterField(
            model_name='eventorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 9, 48, 11, 395421)),
        ),
    ]
