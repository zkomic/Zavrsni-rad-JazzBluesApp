# Generated by Django 3.0 on 2021-08-11 18:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_name', models.CharField(max_length=50)),
                ('street_number', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('postal_code', models.IntegerField()),
                ('country', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('address_details', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_name', models.CharField(max_length=200)),
                ('date_released', models.DateField(default=datetime.date.today)),
                ('album_format', models.CharField(choices=[('vinyl', 'Vinyl 12" Album'), ('cd_album', 'CD Album'), ('cd_box_set', 'CD Box Set')], default=None, max_length=20)),
                ('album_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('in_stock', models.IntegerField()),
                ('number_of_tracks', models.IntegerField()),
                ('number_of_discs', models.IntegerField(default=1)),
                ('album_cover', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=50)),
                ('artist_photo', models.ImageField(blank=True, null=True, upload_to='artists/')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('concert', 'Concert'), ('festival', 'Festival')], default=None, max_length=15)),
                ('event_name', models.CharField(max_length=100)),
                ('event_start_datetime', models.DateTimeField()),
                ('event_end_datetime', models.DateTimeField()),
                ('tickets_sale_start_date', models.DateField()),
                ('event_details', models.CharField(blank=True, max_length=50)),
                ('event_poster', models.ImageField(blank=True, null=True, upload_to='events/')),
                ('ticket_price', models.IntegerField()),
                ('artist_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(choices=[('jazz', 'Jazz'), ('blues', 'Blues')], default=None, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RecordLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recordLabel_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_name', models.CharField(max_length=100)),
                ('row_number', models.IntegerField(null=True)),
                ('row_seat_count', models.IntegerField(null=True)),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('rather_not_say', 'Rather Not Say')], default='rather_not_say', max_length=20)),
                ('address_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Address')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_name', models.CharField(max_length=100)),
                ('duration', models.DurationField(blank=True)),
                ('album_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Album')),
            ],
        ),
        migrations.CreateModel(
            name='TourNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_from_date', models.DateField(default=datetime.date.today)),
                ('publish_to_date', models.DateField()),
                ('news_text', models.CharField(max_length=3000)),
                ('url_link', models.CharField(max_length=150)),
                ('artist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='TicketPurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('processing', 'Processing'), ('sent', 'Sent'), ('canceled', 'Canceled')], default=None, max_length=15)),
                ('order_date', models.DateTimeField()),
                ('seat_number', models.IntegerField()),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Event')),
                ('user_id', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='venue_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Venue'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=250)),
                ('comment', models.CharField(blank=True, max_length=250)),
                ('rating', models.IntegerField(default=1)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('album_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Album')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.PositiveIntegerField()),
                ('quantity', models.IntegerField()),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AlbumOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('canceled', 'Canceled')], default=None, max_length=15)),
                ('album_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Album')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='genre_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.Genre'),
        ),
        migrations.AddField(
            model_name='album',
            name='recordLabel_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='JazzBluesApp.RecordLabel'),
        ),
    ]
