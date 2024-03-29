from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import SplitDateTimeField
from .models import Address, Album, AlbumOrder, Artist, ALBUM_FORMAT_CHOICES, Comment, GENRE_CHOICES, EVENT_CATEGORY_CHOICES, RecordLabel, Event, Venue, Genre
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


class NewAlbumForm(forms.ModelForm):
    artist_id = forms.ModelChoiceField(queryset=Artist.objects.all())
    genre_id = forms.ModelChoiceField(queryset=Genre.objects.all())
    album_name = forms.CharField()
    date_released = forms.DateField(widget=AdminDateWidget(attrs={'type': 'date'}))
    album_format = forms.ChoiceField(choices=ALBUM_FORMAT_CHOICES)
    album_price = forms.DecimalField()
    in_stock = forms.IntegerField()
    number_of_tracks = forms.IntegerField()
    number_of_discs = forms.IntegerField()
    recordLabel_id = forms.ModelChoiceField(queryset=RecordLabel.objects.all())
    album_cover = forms.ImageField(required=False)

    class Meta:
        model = Album
        fields = ["artist_id", "genre_id", "album_name", "date_released", "album_format", "album_price", "in_stock", "number_of_tracks", "number_of_discs", "recordLabel_id", "album_cover"]

class NewArtistForm(forms.ModelForm):
    artist_name = forms.CharField()
    artist_photo = forms.ImageField(required=False)

    class Meta:
        model = Artist
        fields = ["artist_name", "artist_photo"]

class NewRecordLabel(forms.ModelForm):
    recordLabel_name = forms.CharField()
    class Meta:
        model = RecordLabel
        fields = ["recordLabel_name"]

class NewVenueForm(forms.ModelForm):
    location = forms.CharField()
    venue_name = forms.CharField()
    row_number = forms.IntegerField()
    row_seat_count = forms.IntegerField()

    class Meta:
        model = Venue
        fields = ["location", "venue_name", "row_number", "row_seat_count"]

class DateForm(forms.Form):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'date'
        })
    )
class NewEventForm(forms.ModelForm):
    category = forms.ChoiceField(choices=EVENT_CATEGORY_CHOICES, required=False)
    event_start_datetime = forms.SplitDateTimeField()
    event_end_datetime = forms.SplitDateTimeField(required=False)
    available_tickets = forms.IntegerField(required=False)
    class Meta:
        model = Event 
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(NewEventForm, self).__init__(*args, **kwargs)
        self.fields['event_start_datetime'].widget = AdminSplitDateTime()
        self.fields['event_end_datetime'].widget = AdminSplitDateTime()
        
        

class NewAddressForm(forms.ModelForm):
    address_details = forms.CharField(required=False)

    class Meta:
        model = Address 
        fields = '__all__'

class NewComment(forms.ModelForm):  
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rating']


class updateOrderStatus(forms.ModelForm):
    class Meta:
        model = AlbumOrder
        fields = ['order_status']


    
    