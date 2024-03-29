# Generated by Django 3.0 on 2021-08-17 16:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JazzBluesApp', '0035_auto_20210817_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='update_at',
        ),
        migrations.AlterField(
            model_name='albumorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 18, 12, 56, 310781)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(max_length=250),
        ),
        migrations.AlterField(
            model_name='comment',
            name='subject',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='eventorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 17, 18, 12, 56, 310781)),
        ),
    ]
