from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

from django.views.i18n import JavaScriptCatalog

app_name = 'JazzBluesApp'

urlpatterns = [
    url(r'^albums/$', views.albums, name="albums"),
    url(r'^albumsName/$', views.albumsName, name="albumsName"),
    url(r'^albumsNameDesc/$', views.albumsNameDesc, name="albumsNameDesc"),
    url(r'^albumsPrice/$', views.albumsPrice, name="albumsPrice"),
    url(r'^albumsPriceDesc/$', views.albumsPriceDesc, name="albumsPriceDesc"),
    url(r'^events/$', views.events, name="events"),
    url(r'^eventsName/$', views.eventsName, name="eventsName"),
    url(r'^eventsNameDesc/$', views.eventsNameDesc, name="eventsNameDesc"),
    url(r'^eventsPrice/$', views.eventsPrice, name="eventsPrice"),
    url(r'^eventsPriceDesc/$', views.eventsPriceDesc, name="eventsPriceDesc"),
    url(r'^newAlbum/$', views.newAlbum, name="newAlbum"),
    url(r'^newArticle/$', views.newArticle, name="newArticle"),
    url(r'^editArticle/(?P<article_id>\w+)$', views.editArticle, name="editArticle"),
    url(r'^articleDelete/(?P<article_id>\w+)$', views.articleDelete, name="articleDelete"),
    url(r'^newArtist/$', views.newArtist, name="newArtist"),
    url(r'^newRecordLabel/$', views.newRecordLabel, name="newRecordLabel"),
    url(r'^albumEdit/(?P<album_id>\w+)$', views.albumEdit, name="albumEdit"),
    url(r'^addAlbumToCart/(?P<album_id>\w+)$', views.addAlbumToCart, name="addAlbumToCart"),
    url(r'^albumDelete/(?P<album_id>\w+)$', views.albumDelete, name="albumDelete"),
    url(r'^albumDetail/(?P<album_id>\w+)$', views.albumDetail, name="albumDetail"),
    url(r'^addComment/(?P<album_id>\w+)$', views.addComment, name="addComment"),
    url(r'^seats/(?P<event_id>\w+)$', views.seats, name="seats"),
    url(r'^seatReservation/(?P<event_id>\w+)$', views.seatReservation, name="seatReservation"),
    url(r'^eventDetail/(?P<event_id>\w+)$', views.eventDetail, name="eventDetail"),
    url(r'^addEventToCart/(?P<event_id>\w+)$', views.addEventToCart, name="addEventToCart"),
    url(r'^newConcert/$', views.newConcert, name="newConcert"),
    url(r'^newFestival/$', views.newFestival, name="newFestival"),
    url(r'^newVenue/$', views.newVenue, name="newVenue"),
    url(r'^eventEdit/(?P<event_id>\w+)$', views.eventEdit, name="eventEdit"),
    url(r'^addressEdit/(?P<address_id>\w+)$', views.addressEdit, name="addressEdit"),
    url(r'^eventDelete/(?P<event_id>\w+)$', views.eventDelete, name="eventDelete"),
    url(r'^userProfile/(?P<username>\w+)$', views.userProfile, name="userProfile"),
    url(r'^userOrders/(?P<username>\w+)$', views.userOrders, name="userOrders"),
    url(r'^cart/(?P<username>\w+)$', views.cart, name="cart"),
    url(r'^cartAlbumIncrement/(?P<album_id>\w+)$', views.cartAlbumIncrement, name="cartAlbumIncrement"),
    url(r'^cartAlbumDecrement/(?P<album_id>\w+)$', views.cartAlbumDecrement, name="cartAlbumDecrement"),
    url(r'^cartEventIncrement/(?P<event_id>\w+)$', views.cartEventIncrement, name="cartEventIncrement"),
    url(r'^cartEventDecrement/(?P<event_id>\w+)$', views.cartEventDecrement, name="cartEventDecrement"),
    url(r'^orderAddressPayment/(?P<username>\w+)$', views.orderAddressPayment, name="orderAddressPayment"),
    url(r'^checkout/(?P<username>\w+)$', views.checkout, name="checkout"),
    url(r'^staffOrders/$', views.staffOrders, name="staffOrders"),
    url(r'^staffOrderDetail/(?P<albumorder_id>\w+)$', views.staffOrderDetail, name="staffOrderDetail"),
    url(r'^userOrderDetail/(?P<albumorder_id>\w+)$', views.userOrderDetail, name="userOrderDetail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)