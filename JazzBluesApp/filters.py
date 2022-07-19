import django
from django.contrib.admin import widgets
from django.db.models import fields
from django.forms.widgets import CheckboxSelectMultiple, ChoiceWidget, Select
import django_filters
from django_filters import DateFilter, NumberFilter, CharFilter, MultipleChoiceFilter
from django import forms

from .models import *

class ArtistFilter(django_filters.FilterSet):
    class Meta:
        model = Artist
        fields = '__all__'
        exclude = ['artist_photo']

class AlbumFilter(django_filters.FilterSet):
    album_name = django_filters.CharFilter(field_name='album_name', lookup_expr='icontains')
    album_price = django_filters.NumberFilter()
    album_price__gt = django_filters.NumberFilter(field_name='album_price', lookup_expr='gt')
    album_price__lt = django_filters.NumberFilter(field_name='album_price', lookup_expr='lt')
    
    album_format = django_filters.ChoiceFilter(
        choices = ALBUM_FORMAT_CHOICES,
        empty_label = "Select album format ... "
    )

    genre_id = django_filters.ModelChoiceFilter(
        queryset = Genre.objects.all(),
        widget = (),
        label = "Genre",
        empty_label = "Select genre ... ",
    )

    artist_id = django_filters.ModelMultipleChoiceFilter(
        queryset = Artist.objects.all(),
        widget = forms.SelectMultiple(attrs={'id':'artistMultiple','class':'artistMultiple'}),
        label = "Artist",
    )
    class Meta:
        model = Album
        fields= ['artist_id', 'genre_id', 'album_name', 'album_format', 'album_price']

class EventFilter(django_filters.FilterSet):
    event_name = django_filters.CharFilter(field_name='event_name', lookup_expr='icontains')
    artist_id = django_filters.ModelMultipleChoiceFilter(
        queryset = Artist.objects.all(),
        widget = forms.SelectMultiple(attrs={'id':'artistMultiple','class':'artistMultiple'}),
        label = "Artist",
    )


    category = django_filters.ChoiceFilter(
        choices = EVENT_CATEGORY_CHOICES,
        empty_label = "Select category ... "
    )
    class Meta:
        model = Event
        fields = ['artist_id', 'event_name', 'category']

class OrderFilter(django_filters.FilterSet):

    user_id = django_filters.ModelMultipleChoiceFilter(
        queryset = User.objects.all(),
        widget = forms.SelectMultiple(attrs={'id':'userMultiple','class':'userMultiple'}),
        label = "User",
    )

    order_status = django_filters.ChoiceFilter(
        choices = ALBUM_ORDER_STATUS_CHOICES,
        empty_label = "Select order status ... "
    )

    class Meta:
        model = AlbumOrder
        fields = ['user_id', 'order_status']