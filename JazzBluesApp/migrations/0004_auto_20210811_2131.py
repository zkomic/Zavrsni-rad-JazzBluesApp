# Generated by Django 3.0 on 2021-08-11 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('JazzBluesApp', '0003_auto_20210811_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('album_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Album')),
            ],
        ),
        migrations.CreateModel(
            name='AlbumCartUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('albumcart_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.AlbumCart')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Album')),
            ],
        ),
        migrations.CreateModel(
            name='EventCartUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventcart_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.EventCart')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='cartuser',
            name='cart_id',
        ),
        migrations.RemoveField(
            model_name='cartuser',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartUser',
        ),
        migrations.AddField(
            model_name='eventcart',
            name='user_id',
            field=models.ManyToManyField(through='JazzBluesApp.EventCartUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='albumcart',
            name='user_id',
            field=models.ManyToManyField(through='JazzBluesApp.AlbumCartUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
