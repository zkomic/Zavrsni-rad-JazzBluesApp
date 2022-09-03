from types import CoroutineType
from django.db import models
from django.contrib.auth.models import User

from datetime import date, datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

User._meta.get_field('email')._unique = True #email mora biti unique zbog registracije

male = 'male'
female = 'female'
rather_not_say = 'rather_not_say'

GENDER_CHOICES = (
    (male, 'Male'),
    (female, 'Female'),
    (rather_not_say, 'Rather Not Say')
)

class Address (models.Model):
    street_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=50)#možda dodati choices padajući izbornik s državama?
    phone = models.CharField(max_length=20)
    address_details = models.CharField(max_length=100, blank=True)

class Users (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=rather_not_say)
    address_id = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', null=True, blank=True)
    
    def __str__ (self):
        return self.user.username

class RecordLabel (models.Model):
    recordLabel_name = models.CharField(max_length=100)

    def __str__ (self):
        return self.recordLabel_name

class Artist (models.Model):
    artist_name = models.CharField(max_length=50)
    artist_photo = models.ImageField(blank=True, null=True, upload_to="artists/")

    def __str__ (self):
        return self.artist_name

jazz = 'jazz'
blues = 'blues'

GENRE_CHOICES = (
    (jazz, 'Jazz'),
    (blues, 'Blues'),
)

class Genre (models.Model):
    genre_name = models.CharField(max_length=10, choices=GENRE_CHOICES, default=None) 

    def __str__ (self):
        return self.genre_name


vinyl = 'vinyl'
cd_album = 'cd_album'
cd_box_set = 'cd_box_set'

ALBUM_FORMAT_CHOICES = (
    (vinyl, 'Vinyl 12" Album'),
    (cd_album, 'CD Album'),
    (cd_box_set, 'CD Box Set')
)
class Album (models.Model):
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True) #null je true? many to many?
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE, default=1)
    album_name = models.CharField(max_length=200)
    date_released = models.DateField(default=date.today)
    album_format = models.CharField(max_length=20, choices=ALBUM_FORMAT_CHOICES, default=None) 
    album_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    in_stock = models.PositiveIntegerField()
    number_of_tracks = models.IntegerField()
    number_of_discs = models.IntegerField(default=1)
    recordLabel_id = models.ForeignKey(RecordLabel, on_delete=models.CASCADE, null=True) #null je true
    album_cover = models.ImageField(upload_to="albums/", blank=True, null=True)

    def __str__ (self):
        return self.album_name

#class Track (models.Model):
#    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
#    track_name = models.CharField(max_length=100)
#    duration = models.DurationField(blank=True)

#---------------------EVENTS---------------------------
  
class Venue(models.Model):
    location = models.CharField(max_length=100)
    venue_name = models.CharField(max_length=100)
    row_number = models.IntegerField(default=0) #zbog koncerata
    row_seat_count = models.IntegerField(default=0) #zbog koncerata

    def __str__ (self):
        return self.venue_name + ', ' + self.location

concert = 'concert'
festival = 'festival'

EVENT_CATEGORY_CHOICES = (
    (concert, 'Concert'),
    (festival, 'Festival')
)
class Event (models.Model):
    category = models.CharField(max_length=15, choices=EVENT_CATEGORY_CHOICES, default=None, blank=True, null=True)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True)
    event_name = models.CharField(max_length=100)
    event_start_datetime = models.DateTimeField()
    event_end_datetime = models.DateTimeField(blank=True, null=True) #zbog koncerata
    event_details = models.CharField(max_length=50, blank=True)
    event_poster = models.ImageField(blank=True, null=True, upload_to="events/")
    available_tickets = models.PositiveIntegerField(null=True, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__ (self):
        return self.event_name


# ------------------- CARTS --------------------

class AlbumCart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    album_id = models.ManyToManyField(Album, through='AlbumCartUser')
    
class AlbumCartUser(models.Model):
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    albumcart_id = models.ForeignKey(AlbumCart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

class EventCart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event_id = models.ManyToManyField(Event, through='EventCartUser') 

class EventCartUser(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    eventcart_id = models.ForeignKey(EventCart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

# ------------------- ORDERS --------------------

processing = 'processing'
shipped = 'shipped'
sent = 'sent'
canceled = 'canceled'
delivered = 'delivered'

ALBUM_ORDER_STATUS_CHOICES = (
    (processing, 'Processing'),
    (shipped, 'Shipped'),
    (delivered, 'Delivered'),
    (canceled, 'Canceled')
)

class AlbumOrder(models.Model):
   user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   album_id = models.ManyToManyField(Album, through='AlbumOrderUser')
   order_status = models.CharField(max_length=15, choices=ALBUM_ORDER_STATUS_CHOICES, default=processing)
   order_date=models.DateTimeField(default=datetime.now())
   
class AlbumOrderUser(models.Model):
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    albumorder_id = models.ForeignKey(AlbumOrder, on_delete=models.CASCADE, null=True, related_name="albumorderitems")
    quantity = models.IntegerField(default=1)

    @property
    def get_quantity (self):
        return self.quantity
    
class EventOrder(models.Model):
   user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   event_id = models.ManyToManyField(Event, through='EventOrderUser')
   order_date=models.DateTimeField(default=datetime.now())

class EventOrderUser(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    eventorder_id = models.ForeignKey(EventOrder, on_delete=models.CASCADE, null=True, related_name="eventorderitems")
    quantity = models.IntegerField(default=1)

class TicketPurchase(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ManyToManyField(User)
    order_date = models.DateTimeField()
    seat_number = models.IntegerField(null=True)


# ------------------ NEWS -------------------

class Article(models.Model):
    subject = models.CharField(max_length=500)
    publish_date = models.DateField(default=date.today)
    text = models.TextField(max_length=5000)
    image = models.ImageField(upload_to="articles/", blank=True, null=True)


# ------- COMMENTS AND RATING -------

class Comment(models.Model):
    user_id = models.ForeignKey(Users, on_delete=CASCADE)
    album_id = models.ForeignKey(Album, on_delete=CASCADE)
    subject = models.CharField(max_length=250)
    comment = models.TextField(max_length=250)
    rating = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject