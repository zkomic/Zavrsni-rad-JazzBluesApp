# Generated by Django 3.0 on 2021-08-13 17:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JazzBluesApp', '0013_auto_20210813_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='albumorder',
            name='quantity',
        ),
        migrations.AddField(
            model_name='albumorderuser',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='albumorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 13, 19, 44, 58, 920898)),
        ),
        migrations.AlterField(
            model_name='eventorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 13, 19, 44, 58, 920898)),
        ),
    ]
