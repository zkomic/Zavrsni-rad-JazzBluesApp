from django import template
from JazzBluesApp.models import Album, AlbumCartUser, EventCartUser, AlbumOrderUser, EventOrderUser, AlbumOrder, User, AlbumCart, EventCart
from datetime import datetime

register = template.Library()

@register.filter('get_albumCart_quantity')
def get_album_quantity(user_id, albumcart_id):
    albumCart = AlbumCart.objects.filter(user_id=user_id)
    albumUserCart = AlbumCartUser.objects.filter(albumcart_id__in=albumCart)
    for album in albumUserCart:
        if album.album_id == albumcart_id:
            return album.quantity
    return 0

@register.filter('get_albumOrder_quantity')
def get_album_quantity(albumorder_id, album_id):
    albumOrder = AlbumOrder.objects.filter(id=albumorder_id)
    albumUserOrder = AlbumOrderUser.objects.filter(albumorder_id__in=albumOrder)
    print(albumUserOrder)
    for album in albumUserOrder:
        if album.album_id.id == album_id:
            return album.quantity
    return 0



@register.filter('get_event_quantity')
def get_event_quantity(user_id, eventcart_id):
    eventCart = EventCart.objects.filter(user_id=user_id)
    eventUserCart = EventCartUser.objects.filter(eventcart_id__in=eventCart)
    for event in eventUserCart:
        if event.event_id == eventcart_id:
            return event.quantity
    return 0

@register.filter('get_albumorder_quantity')
def get_albumorder_quantity(albumorder_id):
    return AlbumOrderUser.objects.get(album_id=albumorder_id).quantity

@register.filter('get_eventorder_quantity')
def get_eventorder_quantity(eventorder_id):
    return EventOrderUser.objects.get(event_id=eventorder_id).quantity

@register.filter('mult')
def mult(val1, val2):
    return float(val1*val2)

@register.filter('capital')
def capital(status):
    return status.capitalize()

@register.filter('album_total')
def album_total(order_id):
    print(order_id)
    total = 0
    albumOrder = AlbumOrder.objects.filter(id=order_id)
    print(albumOrder)
    albumUserOrder = AlbumOrderUser.objects.filter(albumorder_id__in=albumOrder)
    print(albumUserOrder)
    for album in albumUserOrder:
        print(album.album_id.album_name, album.quantity)
        album_price = Album.objects.get(id=album.album_id.id)
        total = total + album.quantity * album_price.album_price
    return total

@register.filter('get_username')
def get_username(user_id):
    username = User.objects.get(id=user_id)
    return username.username



