from django.contrib import messages
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from JazzBluesApp.models import Album, Article, Artist, Comment, Event, TicketPurchase, Users, Venue, AlbumCart, AlbumCartUser, EventCart, EventCartUser, AlbumOrder, AlbumOrderUser, EventOrder, EventOrderUser
from django.shortcuts import render, redirect
from .forms import NewAlbumForm, NewArtistForm, NewComment, NewRecordLabel, NewEventForm, updateOrderStatus, NewVenueForm, NewArticleForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .filters import AlbumFilter, EventFilter, OrderFilter
from datetime import datetime

#za convert u pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def autocomplete(request):
    if 'term' in request.GET:
        artists = Artist.objects.filter(artist_name__icontains=request.GET.get('term'))
        albums = Album.objects.filter(album_name__icontains=request.GET.get('term'))
        events = Event.objects.filter(event_name__icontains=request.GET.get('term'))
        results = list()
        for artist in artists:
            results.append(artist.artist_name)
        for album in albums:
            results.append(album.album_name)
        for event in events:
            results.append(event.event_name)
        return JsonResponse(results, safe=False)
    return render(request, 'home.html')

def albums(request):

    context = {'orderby': 'albums'}

    if request.method == 'POST':
        orderby = request.POST.get('orderby')
        print(orderby)
        if orderby == 'albums':
            albums = Album.objects.all()
        elif orderby == 'albumsNameAscending':
            albums = Album.objects.all().order_by('album_name')
        elif orderby == 'albumsNameDescending':
            albums = Album.objects.all().order_by('-album_name')
        elif orderby == 'albumsPriceAscending':
            albums = Album.objects.all().order_by('album_price')
        elif orderby == 'albumsPriceDescending':
            albums = Album.objects.all().order_by('-album_price')
        context.update({'orderby': orderby})

    else:
        albums = Album.objects.all()

    albumFilter = AlbumFilter(request.GET, queryset=albums)
    albums = albumFilter.qs

    context.update({
        'albums' : albums,
        'albumFilter' : albumFilter,
    })

    return render(request, 'albums.html', context)

@login_required
@staff_member_required
def newAlbum(request):
    if request.method == 'POST':
        albumForm = NewAlbumForm(request.POST)
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
def newArticle(request):
    if request.method == 'POST':
        articleForm = NewArticleForm(request.POST, request.FILES)
        if articleForm.is_valid():
            articleForm.save()
            return redirect ('base')
    articleForm = NewArticleForm()
    context = {
        'form':articleForm
    }
    return render(request, 'new_article.html', context)

@login_required
@staff_member_required
def editArticle(request, article_id):
    article = Article.objects.all().filter(id=article_id)
    instanca = article.first()
    data = {
        "subject": article[0].subject,
        "publish_date": article[0].publish_date,
        "text": article[0].text,
        "image": article[0].image,
    }
    if request.method == 'POST':
        articleForm = NewArticleForm(request.POST, instance=instanca)
        if articleForm.is_valid():
            articleForm.save()
            return redirect('base')     
    else:
        articleForm = NewArticleForm(initial=data)
    context = {
        'article': article,
        'articleForm': articleForm,
    }
    return render(request, 'article_edit.html', context)

@login_required
@staff_member_required
def articleDelete(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        article.delete()
        return redirect('base')
    except: 
        return redirect('JazzBluesApp:articleEdit', article_id=article_id)

@login_required
@staff_member_required
def albumEdit(request, album_id):
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
        albumForm = NewAlbumForm(request.POST, instance=instanca)
        if albumForm.is_valid():
            albumForm.save()
            return redirect('JazzBluesApp:albums')     
    else:
        albumForm = NewAlbumForm(initial=data)
    context = {
        'artist': album[0].artist_id,
        'recordLabel': album[0].recordLabel_id,
        'albumForm': albumForm,
        'album': album,
    }
    return render(request, 'album_edit.html', context)

def albumDetail(request, album_id):
    album = Album.objects.all().filter(id=album_id)
    related_albums = Album.objects.all().filter(artist_id=album[0].artist_id).exclude(id=album_id)
    comments = Comment.objects.all().filter(album_id=album_id)
    context = {
        'album': album,
        'comments': comments,
        'related_albums': related_albums,
    }
    return render(request, 'album_detail.html', context)

def eventDetail(request, event_id):
    event = Event.objects.all().filter(id=event_id)
    context = {
        'event': event,
    }
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

@login_required
def seats(request, event_id):
    event = Event.objects.get(id=event_id)
    venue = Venue.objects.get(id=event.venue_id.id)
    seat_range = int(venue.row_number) * int(venue.row_seat_count)
    occupied_seats = TicketPurchase.objects.all().filter(event_id=event_id)
    occupied_seat_numbers = []
    for seat in occupied_seats:
        occupied_seat_numbers.append(seat.seat_number)

    context = {
        'event': event,
        'venue': venue,
        'rows': venue.row_number,
        'seats': venue.row_seat_count,
        'range': range(seat_range),
        'occupied': occupied_seat_numbers,
    }
    return render(request, 'seats.html', context)

def seatReservation(request, event_id):
    username = User.objects.get(id=request.user.id).username
    if request.method == 'POST':
        seat_number = request.POST.getlist('seat_number')
        user_id = request.user.id
        print(user_id)
        event = Event.objects.get(id=event_id)
        for seat in seat_number:
            new_ticket = TicketPurchase(event_id=event, order_date=datetime.now(), seat_number=seat)
            new_ticket.save()
            new_ticket.user_id.add(user_id)
    return redirect ('JazzBluesApp:userOrders', username=username)

def events(request):
    events = Event.objects.all()

    eventsFilter = EventFilter(request.GET, queryset=events)
    events = eventsFilter.qs

    context = {
        'events' : events,
        'eventsFilter' : eventsFilter
    }

    return render(request, 'events.html', context)

concert = 'concert'
festival = 'festival'

@login_required
@staff_member_required
def newConcert(request):
    if request.method == 'POST':
        newEventForm = NewEventForm(request.POST)
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
        newEventForm = NewEventForm(request.POST)
        if newEventForm.is_valid():
            newEventForm.save()
            last_event = Event.objects.all().last()
            print(last_event)
            last_event.category = festival
            last_event.save()
            return redirect('JazzBluesApp:events')
    newEventForm = NewEventForm()
    return render(request, 'new_festival.html', {'form': newEventForm})

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
        eventForm = NewEventForm(request.POST, instance=instanca)
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
                print(comment.album_id)
                print(comment.subject)
                print(comment.comment)
                print(comment.rating)
                comment.save()
                messages.success(request, "Your review has been sent. Thank you!")
                return redirect('JazzBluesApp:albumDetail', album_id=album_id)
        else:
            messages.warning(request, "You didn't fill all the fields.")
    return redirect('JazzBluesApp:albumDetail', album_id=album_id) 

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

def userProfile(request, username):
    user = User.objects.get(username=username)
    current_user = Users.objects.get(user=user.id)
    
    
    context = {
        'current_user': current_user,
    }
    return render(request, 'user_profile.html', context)


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
    else:
        pass
    return render(request, 'user_orders.html', context)

def userOrderDetail(request, albumorder_id):
    total = 0

    albumOrder = AlbumOrder.objects.filter(id=albumorder_id)
    albumUserOrder = AlbumOrderUser.objects.filter(albumorder_id__in=albumOrder)
    
    for album in albumUserOrder:
       
        album_price = Album.objects.get(id=album.album_id.id)
        total = total + album.quantity * album_price.album_price
    
    context = {
        'albumOrder': albumOrder[0],
        'total': total,
    }
    return render(request, 'user_order_detail.html', context)


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

def cart(request, username):
    current_user = User.objects.get(username=username)
    context = {'current_user': current_user,}
    total = 0
    if AlbumCart.objects.all().filter(user_id=current_user.id).exists():
        albums = []
        albumCart = AlbumCart.objects.filter(user_id=current_user)
        albumUserCart = AlbumCartUser.objects.filter(albumcart_id__in=albumCart) 
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
        eventUserCart = EventCartUser.objects.filter(eventcart_id__in=eventCart)
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

def checkout(request, username):
    current_user = User.objects.get(username=username) #mozda ne proslijedivati nista? nego requestat?
    album_cart = AlbumCart.objects.filter(user_id=current_user.id)
    event_cart = EventCart.objects.filter(user_id=current_user.id)
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

    



