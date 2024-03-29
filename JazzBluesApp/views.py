from django.contrib import messages
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from JazzBluesApp.models import Album, Artist, Address, Comment, Event, TicketPurchase, Users, Venue, AlbumCart, AlbumCartUser, EventCart, EventCartUser, AlbumOrder, AlbumOrderUser, EventOrder, EventOrderUser
from django.shortcuts import render, redirect
from .forms import NewAlbumForm, NewArtistForm, NewAddressForm, NewComment, NewRecordLabel, NewEventForm, updateOrderStatus, NewVenueForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .filters import AlbumFilter, EventFilter, OrderFilter
from datetime import datetime, date
import urllib
from urllib.parse import urlparse, parse_qs
from django.http import HttpResponseRedirect
from django.urls import reverse

#za convert u pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

#pagination stuff
from django.core.paginator import Paginator

def albums(request):

    albums = Album.objects.all()
    albumFilter = AlbumFilter(request.GET, queryset=albums)
    albums = albumFilter.qs

    # set up pagination
    p = Paginator(albums, 16)
    page = request.GET.get('page')
    albums_paginated = p.get_page(page)

    context = {
        'albums' : albums,
        'albums_paginated' : albums_paginated,
        'albumFilter' : albumFilter,
    }

    return render(request, 'albums.html', context)

def albumsName(request):

    albums = Album.objects.all().order_by('album_name')
    albumFilter = AlbumFilter(request.GET, queryset=albums)
    albums = albumFilter.qs

    p = Paginator(albums, 16)
    page = request.GET.get('page')
    albums_paginated = p.get_page(page)

    context = {
        'albums' : albums,
        'albums_paginated' : albums_paginated,
        'albumFilter' : albumFilter,
    }

    return render(request, 'albums.html', context)

def albumsNameDesc(request):

    albums = Album.objects.all().order_by('-album_name')
    albumFilter = AlbumFilter(request.GET, queryset=albums)
    albums = albumFilter.qs

    # set up pagination
    p = Paginator(albums, 16)
    page = request.GET.get('page')
    albums_paginated = p.get_page(page)

    context = {
        'albums' : albums,
        'albums_paginated' : albums_paginated,
        'albumFilter' : albumFilter,
    }

    return render(request, 'albums.html', context)

def albumsPrice(request):

    albums = Album.objects.all().order_by('album_price')
    albumFilter = AlbumFilter(request.GET, queryset=albums)
    albums = albumFilter.qs

    # set up pagination
    p = Paginator(albums, 16)
    page = request.GET.get('page')
    albums_paginated = p.get_page(page)

    context = {
        'albums' : albums,
        'albums_paginated' : albums_paginated,
        'albumFilter' : albumFilter,
    }

    return render(request, 'albums.html', context)

def albumsPriceDesc(request):

    albums = Album.objects.all().order_by('-album_price')
    albumFilter = AlbumFilter(request.GET, queryset=albums)
    albums = albumFilter.qs

    # set up pagination
    p = Paginator(albums, 16)
    page = request.GET.get('page')
    albums_paginated = p.get_page(page)

    context = {
        'albums' : albums,
        'albums_paginated' : albums_paginated,
        'albumFilter' : albumFilter,
    }

    return render(request, 'albums.html', context)


@login_required
@staff_member_required
def newAlbum(request):
    if request.method == 'POST':
        albumForm = NewAlbumForm(request.POST, request.FILES)
        if albumForm.is_valid():
            albumForm.save()
            return redirect('JazzBluesApp:albums')      
    albumForm = NewAlbumForm()
    context = {
        'form' : albumForm,
    }
    return render(request, 'new_album.html', context)


@login_required
@staff_member_required
def albumEdit(request, album_id):
    prev_url = request.META.get('HTTP_REFERER')
    album = Album.objects.all().filter(id=album_id)
    instanca = album.first()
    data = {
        "artist_id": album[0].artist_id,
        "genre_id": album[0].genre_id,
        "album_name": album[0].album_name,
        "date_released": album[0].date_released,
        "album_format": album[0].album_format,
        "album_price": album[0].album_price,
        "in_stock": album[0].in_stock,
        "number_of_tracks": album[0].number_of_tracks,
        "number_of_discs": album[0].number_of_discs,
        "recordLabel_id": album[0].recordLabel_id,
        "album_cover": album[0].album_cover,
    }
    if request.method == 'POST':
        albumForm = NewAlbumForm(request.POST, request.FILES, instance=instanca)
        if albumForm.is_valid():
            next_url = request.POST.get('next_url')
            albumForm.save()
            return redirect (next_url)     
    else:
        albumForm = NewAlbumForm(initial=data)
    context = {
        'prev_url': prev_url,
        'artist': album[0].artist_id,
        'recordLabel': album[0].recordLabel_id,
        'albumForm': albumForm,
        'album': album,
    }
    return render(request, 'album_edit.html', context)

def albumDetail(request, album_id):
    sum = 0
    album = Album.objects.all().filter(id=album_id)
    related_albums = Album.objects.all().filter(artist_id=album[0].artist_id).exclude(id=album_id)
    comments = Comment.objects.all().filter(album_id=album_id)
    context = {
        'album': album,
        'comments': comments,
        'related_albums': related_albums,
    }
    if comments:
        for comment in comments:
            sum = sum + comment.rating
        average_rating = sum/comments.count()
        context_average = {
            'average_rating': average_rating,
        }
        context.update(context_average)
    
    return render(request, 'album_detail.html', context)

def eventDetail(request, event_id):
    event = Event.objects.all().filter(id=event_id)
    context = {
        'event': event,
    }

    #seats
    this_event = Event.objects.get(id=event_id)
    venue = Venue.objects.get(id=this_event.venue_id.id)
    seat_range = int(venue.row_number) * int(venue.row_seat_count)
    occupied_seats = TicketPurchase.objects.all().filter(event_id=event_id)
    occupied_seat_numbers = []
    for seat in occupied_seats:
        occupied_seat_numbers.append(seat.seat_number)

    context_update = {
        'this_event': this_event,
        'venue': venue,
        'rows': venue.row_number,
        'seats': venue.row_seat_count,
        'range': range(seat_range),
        'occupied': occupied_seat_numbers,
    }
    context.update(context_update)
    return render(request, 'event_detail.html', context)

@login_required
@staff_member_required
def albumDelete(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
        album.delete()
        return redirect('JazzBluesApp:albums')
    except: 
        return redirect('JazzBluesApp:albumEdit', album_id=album_id)

@login_required
@staff_member_required
def newArtist(request):
    prev_url = request.META.get('HTTP_REFERER') 
    if request.method == 'POST':
        artistForm = NewArtistForm(request.POST)
        if artistForm.is_valid():
            next_url = request.POST.get('next_url')
            artistForm.save()
            return redirect (next_url)
    artistForm = NewArtistForm()
    context = {
        'prev_url': prev_url,
        'form': artistForm,
    }
    return render(request, 'new_artist.html', context)

@login_required
@staff_member_required
def newVenue(request):
    prev_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        venueForm = NewVenueForm(request.POST)
        print(venueForm.errors)
        if venueForm.is_valid():
            next_url = request.POST.get('next_url')
            venueForm.save()
            return redirect(next_url)
    venueForm = NewVenueForm()
    context = {
        'form': venueForm,
        'prev_url': prev_url,
    }
    return render(request, 'new_venue.html', context)

@login_required
@staff_member_required #dodati error!!
def newRecordLabel(request):
    prev_url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        recordLabelForm = NewRecordLabel(request.POST)
        if recordLabelForm.is_valid():
            next_url = request.POST.get('next_url')
            recordLabelForm.save()
            return redirect(next_url)
    recordLabelForm = NewRecordLabel()
    context = {
        'form': recordLabelForm,
        'prev_url': prev_url,
    }
    return render(request, 'new_record_label.html', context)

@login_required()
def seatReservation(request, event_id):
    username = User.objects.get(id=request.user.id).username
    #seats
    this_event = Event.objects.get(id=event_id)
    venue = Venue.objects.get(id=this_event.venue_id.id)
    seat_range = int(venue.row_number) * int(venue.row_seat_count)
    occupied_seats = TicketPurchase.objects.all().filter(event_id=event_id)

    context = {
        'event_id': event_id, 
        'this_event': this_event,
        'venue': venue,
        'rows': venue.row_number,
        'seats': venue.row_seat_count,
        'range': range(seat_range),
        'occupied_seats': occupied_seats,
    }

    if request.method == 'POST':
        seat_number = request.POST.getlist('seat_number')
        user_id = request.user.id
        if (seat_number):
            print(seat_number)
            event = Event.objects.get(id=event_id)
            context_update = {
                'reserved': seat_number,
                'current_user': username,
            }
            context.update(context_update)
        else:
            messages.warning(request, "You have to choose seat first.")
            return redirect ('JazzBluesApp:eventDetail', event_id=event_id)
    return render(request, 'seat_reservation_purchase.html', context)

import re
@login_required()
def seatReservationPurchase (request, event_id):
    username = User.objects.get(id=request.user.id).username
    event = Event.objects.get(id=event_id)
    user_id = request.user.id

    if request.method == 'POST':
        reserved_seats = request.POST.get('reserved')
        
        reserved = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d)', reserved_seats)
        for seat in reserved:
            new_ticket = TicketPurchase(event_id=event, order_date=datetime.now(), seat_number=seat)
            new_ticket.save()
            new_ticket.user_id.add(user_id)            
            
    return redirect ('JazzBluesApp:userOrders', username=username)

from datetime import date

def events(request): 

    current_date = date.today()
    events = Event.objects.filter(event_start_datetime__gt = current_date) #printa samo buduće eventove

    eventsFilter = EventFilter(request.GET, queryset=events)
    events = eventsFilter.qs

    #pagination
    p = Paginator(events, 16)
    page = request.GET.get('page')
    events_paginated = p.get_page(page)

    context = {
        'events' : events,
        'events_paginated' : events_paginated,
        'eventsFilter' : eventsFilter
    }

    return render(request, 'events.html', context)

@login_required()
@staff_member_required()
def eventsStaff(request):

    events = Event.objects.all() #printa sve eventove

    eventsFilter = EventFilter(request.GET, queryset=events)
    events = eventsFilter.qs

    # set up pagination
    p = Paginator(events, 16)
    page = request.GET.get('page')
    events_paginated = p.get_page(page)

    context = {
        'events' : events,
        'events_paginated' : events_paginated,
        'eventsFilter' : eventsFilter
    }

    return render(request, 'events.html', context)


def eventsName(request):

    current_date = date.today()
    events = Event.objects.filter(event_start_datetime__gt = current_date).order_by('event_name')

    eventsFilter = EventFilter(request.GET, queryset=events)
    events = eventsFilter.qs

    p = Paginator(events, 16)
    page = request.GET.get('page')
    events_paginated = p.get_page(page)

    context = {
        'events' : events,
        'events_paginated' : events_paginated,
        'eventsFilter' : eventsFilter
    }

    return render(request, 'events.html', context)

def eventsNameDesc(request):

    current_date = date.today()
    events = Event.objects.filter(event_start_datetime__gt = current_date).order_by('-event_name')

    eventsFilter = EventFilter(request.GET, queryset=events)
    events = eventsFilter.qs

    p = Paginator(events, 16)
    page = request.GET.get('page')
    events_paginated = p.get_page(page)

    context = {
        'events' : events,
        'events_paginated' : events_paginated,
        'eventsFilter' : eventsFilter
    }

    return render(request, 'events.html', context)

def eventsPrice(request):

    current_date = date.today()
    events = Event.objects.filter(event_start_datetime__gt = current_date).order_by('ticket_price')

    eventsFilter = EventFilter(request.GET, queryset=events)
    events = eventsFilter.qs

    # set up pagination
    p = Paginator(events, 16)
    page = request.GET.get('page')
    events_paginated = p.get_page(page)

    context = {
        'events' : events,
        'events_paginated' : events_paginated,
        'eventsFilter' : eventsFilter
    }

    return render(request, 'events.html', context)

def eventsPriceDesc(request):

    current_date = date.today()
    events = Event.objects.filter(event_start_datetime__gt = current_date).order_by('-ticket_price')

    eventsFilter = EventFilter(request.GET, queryset=events)
    events = eventsFilter.qs

    # set up pagination
    p = Paginator(events, 16)
    page = request.GET.get('page')
    events_paginated = p.get_page(page)

    context = {
        'events' : events,
        'events_paginated' : events_paginated,
        'eventsFilter' : eventsFilter
    }

    return render(request, 'events.html', context)

concert = 'concert'
festival = 'festival'

@login_required
@staff_member_required
def newConcert(request):
    if request.method == 'POST':
        newEventForm = NewEventForm(request.POST, request.FILES)
        if newEventForm.is_valid():
            newEventForm.save()
            last_event = Event.objects.all().last()
            print(last_event)
            last_event.category = concert
            last_event.save()
            return redirect('JazzBluesApp:events')
    newEventForm = NewEventForm()
    return render(request, 'new_concert.html', {'form': newEventForm})

@login_required
@staff_member_required
def newFestival(request):
    if request.method == 'POST':
        newEventForm = NewEventForm(request.POST, request.FILES)
        if newEventForm.is_valid():
            newEventForm.save()
            last_event = Event.objects.all().last()
            print(last_event)
            last_event.category = festival
            last_event.save()
            return redirect('JazzBluesApp:events')
    newEventForm = NewEventForm()
    return render(request, 'new_festival.html', {'form': newEventForm})

@login_required()
@staff_member_required()
def eventEdit(request, event_id):
    event = Event.objects.all().filter(id=event_id)
    instanca = event.first()
    data = {
        "category": event[0].category,
        "artist_id": event[0].artist_id,
        "venue_id": event[0].venue_id,
        "event_name": event[0].event_name,
        "event_start_datetime": event[0].event_start_datetime,
        "event_end_datetime": event[0].event_end_datetime,
        "available_tickets": event[0].available_tickets,
        "event_details": event[0].event_details,
        "event_poster": event[0].event_poster,
        "ticket_price": event[0].ticket_price,
    }
    if request.method == 'POST':
        eventForm = NewEventForm(request.POST, request.FILES, instance=instanca)
        print(eventForm.errors)
        if eventForm.is_valid():
            eventForm.save()
            return redirect('JazzBluesApp:eventDetail', event_id=event[0].id)     
    else:
        eventForm = NewEventForm(initial=data)
    context = {
        'eventForm': eventForm,
        'event': event,
    }
    return render(request, 'event_edit.html', context)

@login_required
@staff_member_required
def eventDelete(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        event.delete()
        return redirect('JazzBluesApp:events')
    except: 
        return redirect('JazzBluesApp:eventEdit', event_id=event_id)

def addComment(request, album_id):
    if request.method == 'POST':
        form = NewComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            user = User.objects.get(id=request.user.id)
            current_user = Users.objects.get(user=user)
            #print(current_user)
            comment.user_id = current_user
            comment.album_id = Album.objects.get(id = album_id)
            if comment.subject and comment.comment and comment.rating: 
                comment.save()
                messages.success(request, "Your review has been sent. Thank you!")
                return redirect('JazzBluesApp:albumDetail', album_id=album_id)
        else:
            messages.warning(request, "You didn't fill all the fields.")
    return redirect('JazzBluesApp:albumDetail', album_id=album_id) 

@login_required()
@staff_member_required
def staffOrders(request):
    orders_list = AlbumOrder.objects.all().order_by('-id')
    orderFilter = OrderFilter(request.GET, queryset=orders_list)
    orders_list = orderFilter.qs

    orders = []
    id = []
    for order in orders_list:
        for order.album_id_id in order.album_id.all():
            if int(order.id) not in id:
                id.append(order.id)
                orders.append([order, order.album_id_id.album_name])
    context = {
        'orders': orders,
        'orderFilter': orderFilter,
        'orders_list': orders_list,
    }
    return render(request, 'staff_orders.html', context)

@login_required()
@staff_member_required()
def staffOrderDetail(request, albumorder_id):
    albumOrder = AlbumOrder.objects.filter(id=albumorder_id)
    albumUserOrder = AlbumOrderUser.objects.filter(albumorder_id__in=albumOrder)
    total = 0

    for album in albumUserOrder:
       
        album_price = Album.objects.get(id=album.album_id.id)
        total = total + album.quantity * album_price.album_price

    data = {
        "order_status": albumOrder[0].order_status,
    }
    if request.method == 'POST':
        updateOrderStatusForm = updateOrderStatus(request.POST, instance=albumOrder[0])
        if updateOrderStatusForm.is_valid():
            updateOrderStatusForm.save()
            return redirect('JazzBluesApp:staffOrders')
    #updateOrderStatusForm = updateOrderStatus(initial=data)
    else:
        updateOrderStatusForm = updateOrderStatus(initial=data)
    context = {
        'albumOrder': albumOrder[0],
        'updateOrderStatusForm': updateOrderStatusForm,
        'total': total,
    }
    return render(request, 'staff_order_detail.html', context)

@login_required()
def userProfile(request, username):
    user = User.objects.get(username=username)
    current_user = Users.objects.get(user=user.id)
    
    
    context = {
        'current_user': current_user,
    }
    return render(request, 'user_profile.html', context)

@login_required()
def userOrders(request, username):
    current_user = User.objects.get(username=username)
    tickets = TicketPurchase.objects.all().filter(user_id=current_user.id)
    context = {
        'current_user': current_user,
        'tickets': tickets,
    }
    if AlbumOrder.objects.all().filter(user_id=current_user.id).exists():
        userAlbumOrder = AlbumOrder.objects.all().filter(user_id=current_user).order_by('-id')
        total = 0
        albumOrders = []
        for albumOrder in userAlbumOrder:
            albumOrders.append(albumOrder)
            album_dict = {
                'albumOrders': albumOrders,
                'total': total,
            }
            context.update(album_dict)
        else:
            pass 
    if EventOrder.objects.all().filter(user_id=current_user.id).exists():
        userEventOrder = EventOrder.objects.all().filter(user_id=current_user).order_by('-id')
        total = 0
        eventOrders = []
        for eventOrder in userEventOrder:
            eventOrders.append(eventOrder)
            event_dict = {
                'eventOrders': eventOrders,
                'total': total,
            }
        context.update(event_dict)  
    else:
        pass
    return render(request, 'user_orders.html', context)

@login_required()
def userOrderDetail(request, albumorder_id):
    total = 0

    current_user = User.objects.get(username=request.user.username)
    context = {'current_user': current_user,}
    #total = 0

    albumOrder = AlbumOrder.objects.filter(id=albumorder_id)
    albumUserOrder = AlbumOrderUser.objects.filter(albumorder_id__in=albumOrder)
    
    for album in albumUserOrder:
       
        album_price = Album.objects.get(id=album.album_id.id)
        total = total + album.quantity * album_price.album_price
   
    
    album_order = {
        'albumOrder': albumOrder[0], 
        'total': total,
    }
    context.update(album_order)

    return render(request, 'user_order_detail.html', context)

def userConcertTicketDetail(request, ticketpurchase_id):

    ticketPurchase = TicketPurchase.objects.filter(id=ticketpurchase_id)
    event = Event.objects.get(id=ticketPurchase[0].event_id_id)

    context = {
        'ticketPurchase': ticketPurchase[0],
        'event': event,
    }
    return render(request, 'user_ticket_detail.html', context)

def userFestivalTicketDetail(request, eventorder_id):

    eventOrder = EventOrder.objects.filter(id=eventorder_id)
    eventUserOrder = EventOrderUser.objects.filter(eventorder_id__in=eventOrder)
    event = Event.objects.get(id=eventUserOrder[0].event_id_id)

    context = {
        'eventOrder': eventOrder[0],
        'event': event,
    }
    return render(request, 'user_ticket_detail.html', context)

#----------------------------- CART AND CHECKOUT -----------------------------

@login_required
def addAlbumToCart(request, album_id):
    user = User.objects.get(id=request.user.id)
    album = Album.objects.get(id=album_id)
    try:
        userCart = AlbumCart.objects.get(user_id=user)
        print(userCart)
        userCart.album_id.add(album)
    except:
        album_cart = AlbumCart(user_id=user)
        album_cart.save()
        album_cart.album_id.add(album)
    return redirect('JazzBluesApp:albums')

@login_required
def addEventToCart(request, event_id):
    user = User.objects.get(id=request.user.id)
    event = Event.objects.get(id=event_id)
    try:
        userCart = EventCart.objects.get(user_id=user)
        userCart.event_id.add(event) 
    except:
        event_cart = EventCart(user_id=user)
        event_cart.save()
        event_cart.event_id.add(event)
    return redirect('JazzBluesApp:events')

@login_required()
def cart(request, username):
    current_user = User.objects.get(username=username)
    context = {'current_user': current_user,}
    total = 0
    if AlbumCart.objects.all().filter(user_id=current_user.id).exists():
        albums = []
        albumCart = AlbumCart.objects.filter(user_id=current_user)
        albumUserCart = AlbumCartUser.objects.filter(albumcart_id__in=albumCart).order_by('-id')
        for album in albumUserCart: 
            albums.append(album.album_id)
            album_price = Album.objects.get(id=album.album_id.id) 
            total = total + album.quantity * album_price.album_price 
        
        album_dict = {
            'userAlbumCart': albumCart[0],
            'albums': albums,
            'total': total,
        }
        context.update(album_dict)
    else:
        pass
    if EventCart.objects.all().filter(user_id=current_user).exists():
        events = []
        eventCart = EventCart.objects.filter(user_id=current_user)
        eventUserCart = EventCartUser.objects.filter(eventcart_id__in=eventCart).order_by('-id')
        for event in eventUserCart: 
            events.append(event.event_id)
            ticket_price = Event.objects.get(id=event.event_id.id) 
            total = total + event.quantity * ticket_price.ticket_price 
        event_dict = {
            'userEventCart': eventCart[0],
            'events': events,
            'total': total
        }
        context.update(event_dict)
    else:
        pass
    return render(request, 'cart.html', context)

@login_required()
def orderAddressPayment(request, username):
    current_user = User.objects.get(username=username)
    user_address = Users.objects.get(user=current_user)
    context = {'current_user': current_user,'user_address':user_address }
    total = 0
    if AlbumCart.objects.all().filter(user_id=current_user.id).exists():
        albums = []
        albumCart = AlbumCart.objects.filter(user_id=current_user)
        albumUserCart = AlbumCartUser.objects.filter(albumcart_id__in=albumCart).order_by('-id')
        for album in albumUserCart: 
            albums.append(album.album_id)
            album_price = Album.objects.get(id=album.album_id.id) 
            total = total + album.quantity * album_price.album_price 
        
        album_dict = {
            'userAlbumCart': albumCart[0],
            'albums': albums,
            'total': total,
        }
        context.update(album_dict)
    else:
        pass
    if EventCart.objects.all().filter(user_id=current_user).exists():
        events = []
        eventCart = EventCart.objects.filter(user_id=current_user)
        eventUserCart = EventCartUser.objects.filter(eventcart_id__in=eventCart).order_by('-id')
        for event in eventUserCart: 
            events.append(event.event_id)
            ticket_price = Event.objects.get(id=event.event_id.id) 
            total = total + event.quantity * ticket_price.ticket_price 
        event_dict = {
            'userEventCart': eventCart[0],
            'events': events,
            'total': total
        }
        context.update(event_dict)
    else:
        pass
    return render(request, 'order_address_payment.html', context)


def cartAlbumIncrement(request, album_id):
    current_user = User.objects.get(id=request.user.id)
    try:
        albumCart = AlbumCart.objects.filter(user_id=current_user)
        albumUserCart = AlbumCartUser.objects.filter(albumcart_id__in=albumCart)
        for album in albumUserCart:
            if int(album.album_id.id) == int(album_id):
                stock = Album.objects.get(id=album_id)
                if Album.objects.get(id=album_id).in_stock >= (album.quantity + 1):
                    album.quantity += 1
                    album.save()
                else:
                    messages.warning(request, "No more albums available!")            
    except:
        return redirect('JazzBluesApp:cart', username=current_user.username) 
    return redirect('JazzBluesApp:cart', username=current_user.username)

def cartAlbumDecrement(request, album_id):
    current_user = User.objects.get(id=request.user.id)
    try:
        albumCart = AlbumCart.objects.filter(user_id=current_user)
        albumUserCart = AlbumCartUser.objects.filter(albumcart_id__in=albumCart)
        cart_count = albumUserCart.count()
        for album in albumUserCart:
            if int(album.album_id.id) == int(album_id):
                if album.quantity == 1:
                    album.delete()
                    if cart_count == 1:
                        albumCart.delete()
                else:
                    album.quantity -= 1
                    album.save()              
    except:
        return redirect('JazzBluesApp:cart', username=current_user.username) 
    return redirect('JazzBluesApp:cart', username=current_user.username)

def cartEventIncrement(request, event_id):
    current_user = User.objects.get(id=request.user.id)
    try:
        eventCart = EventCart.objects.filter(user_id=current_user)
        eventUserCart = EventCartUser.objects.filter(eventcart_id__in=eventCart)
        for event in eventUserCart:
            if int(event.event_id.id) == int(event_id):
                stock = Event.objects.get(id=event_id)
                if Event.objects.get(id=event_id).available_tickets >= (event.quantity + 1):
                    event.quantity += 1
                    event.save()
                else:
                    messages.warning(request, "No more tickets available!")            
    except:
        return redirect('JazzBluesApp:cart', username=current_user.username) 
    return redirect('JazzBluesApp:cart', username=current_user.username)

def cartEventDecrement(request, event_id):
    current_user = User.objects.get(id=request.user.id)
    try:
        eventCart = EventCart.objects.filter(user_id=current_user)
        eventUserCart = EventCartUser.objects.filter(eventcart_id__in=eventCart)
        cart_count = eventUserCart.count()
        for event in eventUserCart:
            if int(event.event_id.id) == int(event_id):
                if event.quantity == 1:
                    event.delete()
                    if cart_count == 1:
                        eventCart.delete()
                else:
                    event.quantity -= 1
                    event.save()              
    except:
        return redirect('JazzBluesApp:cart', username=current_user.username) 
    return redirect('JazzBluesApp:cart', username=current_user.username)

@login_required()
def checkout(request, username):
    current_user = User.objects.get(username=username) #mozda ne proslijedivati nista? nego requestat?
    album_cart = AlbumCart.objects.filter(user_id=current_user.id)
    event_cart = EventCart.objects.filter(user_id=current_user.id)
    print(album_cart)
    if album_cart.exists():
        userAlbumCart = AlbumCartUser.objects.filter(albumcart_id__in=album_cart)
        order_item = AlbumOrder(user_id=current_user)
        order_item.save()
        for album in userAlbumCart:
            order_details = AlbumOrderUser(albumorder_id=order_item)
            order_details.quantity = album.quantity
            to_update = Album.objects.get(id=album.album_id.id)
            to_update.in_stock = int(to_update.in_stock) - int (album.quantity)
            to_update.save()
            order_details.album_id = album.album_id
            order_details.save()
        album_cart.delete()
    else:
        pass
    if event_cart.exists():
        userEventCart = EventCartUser.objects.filter(eventcart_id__in=event_cart)
        order_item = EventOrder(user_id=current_user)
        order_item.save()
        for event in userEventCart:
            order_details = EventOrderUser(eventorder_id=order_item)
            order_details.quantity = event.quantity
            to_update = Event.objects.get(id=event.event_id.id)
            to_update.available_tickets = int(to_update.available_tickets) - int (event.quantity)
            to_update.save()
            order_details.event_id = event.event_id
            order_details.save()
        event_cart.delete()
    else:
        pass
    return redirect('JazzBluesApp:userOrders', username=username)

@login_required()
def newAddress(request):
    prev_url = request.META.get('HTTP_REFERER')
    user = User.objects.get(id=request.user.id)
    current_user = Users.objects.get(user=user)
    if request.method == 'POST':
        addressForm = NewAddressForm(request.POST or None)
        if addressForm.is_valid():
            next_url = request.POST.get('next_url')
            print(next_url)
            addressForm.save()
            newUserAddress = Address.objects.last()
            current_user.address_id = newUserAddress
            current_user.save()
            return redirect (next_url)
    addressForm = NewAddressForm()
    context = {
        'prev_url': prev_url,
        'form': addressForm,
    }
    return render(request, 'new_address.html', context)

@login_required()
def addressEdit(request, address_id):
    prev_url = request.META.get('HTTP_REFERER')
    address = Address.objects.all().filter(id=address_id)
    instanca = address.first()
    data = {
        "street_name": address[0].street_name,
        "street_number": address[0].street_number,
        "city": address[0].city,
        "postal_code": address[0].postal_code,
        "country": address[0].country,
        "phone": address[0].phone,
        "address_details": address[0].address_details,
    }
    if request.method == 'POST':
        addressForm = NewAddressForm(request.POST, instance=instanca)
        print(addressForm.errors)
        if addressForm.is_valid():
            next_url = request.POST.get('next_url')
            addressForm.save()
            return redirect (next_url)  
    else:
        addressForm = NewAddressForm(initial=data)
    context = {
        'prev_url': prev_url,
        'addressForm': addressForm,
        'address': address,
    }
    return render(request, 'address_edit.html', context)

