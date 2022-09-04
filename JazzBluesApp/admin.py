from django.contrib import admin
from .models import Comment, EventOrder, EventOrderUser, RecordLabel, Artist, Genre, Album, Users, Venue, Event, AlbumOrder, TicketPurchase, Users, Address, AlbumCart, EventCart, AlbumCartUser, EventCartUser, AlbumOrderUser

# Register your models here.

admin.site.register(Users)
admin.site.register(RecordLabel)
admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Album)
#admin.site.register(Track)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(TicketPurchase)
#admin.site.register(Article)
admin.site.register(Address)
admin.site.register(Comment)
admin.site.register(AlbumCart)
admin.site.register(AlbumCartUser)
admin.site.register(EventCart)
admin.site.register(EventCartUser)
admin.site.register(AlbumOrder)
admin.site.register(AlbumOrderUser)
admin.site.register(EventOrder)
admin.site.register(EventOrderUser)





