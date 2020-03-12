from datetime import datetime, date
from django.views import View
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.views import View
from .utils import render_to_pdf
from .forms import *


def web(request):
    sliders = Slider.objects.all()
    abouts = About.objects.all()
    accommodations = Accommodation.published.all()[:3]
    events = Event.published.all()[:3]

    context = {
        'sliders': sliders,
        'abouts': abouts,
        'accommodations': accommodations,
        'events': events,
    }
    return render(request, 'home/index_public.html', context)



def dashboard(request):
    return render(request, 'home/home.html')


def contact(request):
    if request.method == 'POST':
        f = FeedbackForm(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'Feedback Submitted.')
            return redirect('contact')
    else:
        f = FeedbackForm()
    return render(request, 'home/contacts.html', {'form': f})


# ###################################===>BEGINNING OF SLIDER MODULE<===################################################

# ###################################===>BEGINNING OF ABOUT MODULE<===#################################################


class AboutListView(ListView):
    model = About
    template_name = 'abouts/about_list.html'
    context_object_name = 'abouts'



class AboutCreateView(CreateView):
    model = About
    template_name = 'abouts/about_create.html'
    fields = ('about', 'about_image')

    def form_valid(self, form):
        about = form.save(commit=False)
        about.save()
        return redirect('about_list')



class AboutUpdateView(UpdateView):
    model = About
    template_name = 'abouts/update_about.html'
    pk_url_kwarg = 'about_pk'
    fields = ('about', 'about_image')

    def form_valid(self, form):
        about = form.save(commit=False)
        about.save()
        return redirect('about_list')


@login_required
def save_about_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            abouts = About.objects.all()
            data['html_about_list'] = render_to_string('abouts/includes/partial_about_list.html', {
                'abouts': abouts
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def about_view(request, about_pk):
    about = get_object_or_404(About, pk=about_pk)
    if request.method == 'POST':
        form = AboutForm(request.POST, instance=about)
    else:
        form = AboutForm(instance=about)
    return save_about_form(request, form, 'abouts/includes/partial_about_view.html')


def about_detail(request, about_pk):
    about = get_object_or_404(About, pk=about_pk)
    context = {
        'about': about,
    }
    return render(request, 'abouts/about_detail.html', context)


@login_required
def about_delete(request, about_pk):
    about = get_object_or_404(About, pk=about_pk)
    data = dict()
    if request.method == 'POST':
        about.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        abouts = About.objects.all()
        data['html_about_list'] = render_to_string('abouts/includes/partial_about_list.html', {
            'abouts': abouts
        })
    else:
        context = {'about': about}
        data['html_form'] = render_to_string('abouts/includes/partial_about_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ABOUT MODULE<===##################################################

class SliderListView(ListView):
    model = Slider
    template_name = 'sliders/slider_list.html'
    context_object_name = 'sliders'


class SliderCreateView(CreateView):
    model = Slider
    template_name = 'sliders/slider_create.html'
    fields = ('slider_image', 'image_title')

    def form_valid(self, form):
        slider = form.save(commit=False)
        slider.save()
        return redirect('slider_list')


class SliderUpdateView(UpdateView):
    model = Slider
    template_name = 'sliders/update_slider.html'
    pk_url_kwarg = 'slider_pk'
    fields = ('slider_image', 'image_title')

    def form_valid(self, form):
        slider = form.save(commit=False)
        slider.save()
        return redirect('slider_list')


def save_slider_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sliders = Slider.objects.all()
            data['html_slider_list'] = render_to_string('sliders/includes/partial_slider_list.html', {
                'sliders': sliders
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def slider_view(request, slider_pk):
    slider = get_object_or_404(Slider, pk=slider_pk)
    if request.method == 'POST':
        form = SliderForm(request.POST, instance=slider)
    else:
        form = SliderForm(instance=slider)
    return save_slider_form(request, form, 'sliders/includes/partial_slider_view.html')


@login_required
def slider_delete(request, slider_pk):
    slider = get_object_or_404(Slider, pk=slider_pk)
    data = dict()
    if request.method == 'POST':
        slider.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        sliders = Slider.objects.all()
        data['html_slider_list'] = render_to_string('sliders/includes/partial_slider_list.html', {
            'sliders': sliders
        })
    else:
        context = {'slider': slider}
        data['html_form'] = render_to_string('sliders/includes/partial_slider_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF SLIDER MODULE<===##################################################

# ###################################===>BEGINNING OF NEWS MODULE<===#################################################


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'


def news_wall(request):
    news = News.published.all()
    return render(request, 'news/news_wall.html', {'news': news})


class NewsCreateView(CreateView):
    model = News
    template_name = 'news/news_create.html'
    fields = ('news_title', 'image', 'news', 'Is_View_on_Web')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.author = self.request.user
        news.save()
        return redirect('news_list')


class NewsUpdateView(UpdateView):
    model = News
    template_name = 'news/update_news.html'
    pk_url_kwarg = 'news_pk'
    fields = ('news_title', 'image', 'news', 'Is_View_on_Web')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.save()
        return redirect('news_list')


@login_required
def save_news_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            newss = News.objects.all()
            data['html_news_list'] = render_to_string('news/includes/partial_news_list.html', {
                'news': newss
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def news_view(request, news_pk):
    news = get_object_or_404(News, pk=news_pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
    else:
        form = NewsForm(instance=news)
    return save_news_form(request, form, 'news/includes/partial_news_view.html')


def news_detail(request, news_pk):
    news = get_object_or_404(News, pk=news_pk)
    more_news = News.published.order_by('-date')[:5]
    context = {
        'news': news,
        'more_news': more_news
    }
    return render(request, 'news/news_detail.html', context)


@login_required
def news_delete(request, news_pk):
    news = get_object_or_404(News, pk=news_pk)
    data = dict()
    if request.method == 'POST':
        news.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        news = News.objects.all()
        data['html_news_list'] = render_to_string('news/includes/partial_news_list.html', {
            'news': news
        })
    else:
        context = {'news': news}
        data['html_form'] = render_to_string('news/includes/partial_news_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF NEWS MODULE<===####################################################

# ###################################===>BEGINNING OF EVENT MODULE<===#################################################


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'


def event_wall(request):
    events = Event.published.all()
    return render(request, 'events/events_wall.html', {'events': events})


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event_create.html'
    fields = ('event_title', 'event_for', 'price', 'event_place', 'from_date', 'to_date', 'image', 'note',
              'Is_View_on_Web')

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        return redirect('event_list')


class EventUpdateView(UpdateView):
    model = Event
    template_name = 'events/update_event.html'
    pk_url_kwarg = 'event_pk'
    fields = ('event_title', 'event_for', 'price', 'event_place', 'from_date', 'to_date', 'image', 'note',
              'Is_View_on_Web')

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        return redirect('event_list')


@login_required
def save_event_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            events = Event.objects.all()
            data['html_event_list'] = render_to_string('events/includes/partial_event_list.html', {
                'events': events
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def event_view(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
    else:
        form = EventForm(instance=event)
    return save_event_form(request, form, 'events/includes/partial_cab_view.html')


def event_detail(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    more_events = Event.published.order_by('-from_date')[:5]
    context = {
        'event': event,
        'more_events': more_events
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def event_delete(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    data = dict()
    if request.method == 'POST':
        event.delete()
        data['form_is_valid'] = True
        events = Event.objects.all()
        data['html_event_list'] = render_to_string('events/includes/partial_event_list.html', {
            'events': events
        })
    else:
        context = {'event': event}
        data['html_form'] = render_to_string('events/includes/partial_event_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


@login_required
def book_trip(request, trip_pk):
    trip = get_object_or_404(Event, pk=trip_pk)
    price = trip.price

    context = {
        'price': price,
        'trip': trip
    }
    return render(request, 'events/booking.html', context)


@login_required
def reserve_trip_slot(request, trip_pk):
    if request.method == 'POST':
        Firstname = request.POST.get('firstname')
        Lastname = request.POST.get('lastname')
        user = request.user
        trip = Event.objects.get(id=trip_pk)
        new_booking = TripBooking()
        new_booking.trip = trip
        new_booking.user = user
        new_booking.tourist_first_name = Firstname
        new_booking.tourist_last_name = Lastname
        new_booking.save()
        link = reverse('user_trip_bookings')
        return HttpResponseRedirect(link)
    else:
        url = reverse('user_trip_bookings')
        return url


@login_required
def user_trip_bookings(request):
    bookings = TripBooking.objects.filter(user=request.user)
    context = {'bookings': bookings}
    return render(request, 'events/mybookings.html', context)


@login_required
def cancel_trip_booking(request, trip_pk):
    booking = TripBooking.objects.get(id=trip_pk)
    booking.delete()
    currentuser = request.user
    link = reverse('user_trip_bookings')
    return HttpResponseRedirect(link)


class GenerateTripPDF(View):
    def get(self, request, *args, **kwargs):
        booking = TripBooking.objects.get(id=self.kwargs['trip_pk'])
        template = get_template('events/invoice.html')
        context = {"booking": booking}
        html = template.render(context)
        pdf = render_to_pdf('events/invoice.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


class EventReviewCreateView(CreateView):
    model = EventReview
    fields = ['comment', 'rating']

    def get_success_url(self):
        event_pk = self.kwargs['id']
        url = reverse('event_detail', args=[event_pk])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.event_id = self.kwargs['id']
        return super(EventReviewCreateView, self).form_valid(form)


class EventReviewUpdateView(UpdateView):
    model = EventReview
    fields = ['comment', 'rating']

    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = EventReview.objects.get(id=review_pk)
        event = review.event
        event_pk = event.id
        url = reverse('event_detail', args=[event_pk])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventReviewUpdateView, self).form_valid(form)


class EventReviewDeleteView(DeleteView):
    model = EventReview

    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = EventReview.objects.get(id=review_pk)
        event = review.event
        event_pk = event.id
        url = reverse('event_detail', args=[event_pk])
        return url


# #######################################===>END OF EVENT MODULE<===##################################################

# ###################################===>BEGINNING OF ACCOMMODATION MODULE<===#########################################


class AccommodationListView(ListView):
    model = Accommodation
    template_name = 'accommodations/accommodation_list.html'
    context_object_name = 'accommodations'


# def accommodation_wall(request):
#     accommodations = Accommodation.published.all()
#     return render(request, 'accommodations/route_wall.html', {'accommodations': accommodations})


class AccommodationCreateView(CreateView):
    model = Accommodation
    template_name = 'accommodations/accommodation_create.html'
    fields = ('name', 'code', 'image', 'lowest_charge', 'address')

    def form_valid(self, form):
        accommodation = form.save(commit=False)
        accommodation.save()
        return redirect('accommodation_list')


class AccommodationUpdateView(UpdateView):
    model = Accommodation
    template_name = 'accommodations/update_accommodation.html'
    pk_url_kwarg = 'accommodation_pk'
    fields = ('name', 'code', 'image', 'lowest_charge', 'address')

    def form_valid(self, form):
        accommodation = form.save(commit=False)
        accommodation.save()
        return redirect('accommodation_list')


def save_accommodation_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            accommodations = Accommodation.objects.all()
            data['html_accommodation_list'] = render_to_string(
                'accommodations/includes/partial_accommodation_list.html', {
                    'accommodations': accommodations
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def accommodation_view(request, accommodation_pk):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_pk)
    if request.method == 'POST':
        form = AccommodationForm(request.POST, instance=accommodation)
    else:
        form = AccommodationForm(instance=accommodation)
    return save_accommodation_form(request, form, 'accommodations/includes/partial_accommodation_view.html')


def accommodation_detail(request, accommodation_pk):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_pk)

    rooms = Room.objects.filter(accommodation=accommodation)
    city = accommodation.address
    FirstDate = request.session['checkin']
    SecDate = request.session['checkout']
    current_user = request.user
    for room in rooms:
        RoomsBooked = Reservation.objects.filter(room=room).filter(CheckIn__lte=SecDate,
                                                                   CheckOut__gte=FirstDate)
        count = RoomsBooked.count()
        count = int(count)
        Roomsavailable = room.totalRooms
        Roomsavailable = int(Roomsavailable)

        Roomsleft = Roomsavailable - count
        room.spaceleft = Roomsleft

    context = {
        'accommodation': accommodation,
        'user': current_user,
        'rooms': rooms,
        'city': city
    }
    return render(request, 'accommodations/accommodation_detail.html', context)


@login_required
def accommodation_delete(request, accommodation_pk):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_pk)
    data = dict()
    if request.method == 'POST':
        accommodation.delete()
        data['form_is_valid'] = True
        accommodations = Accommodation.objects.all()
        data['html_accommodation_list'] = render_to_string('accommodations/includes/partial_accommodation_list.html', {
            'accommodations': accommodations
        })
    else:
        context = {'accommodation': accommodation}
        data['html_form'] = render_to_string('accommodations/includes/partial_accommodation_delete.html',
                                             context, request=request)
    return JsonResponse(data)


class accommodation_search(View):
    def get(self, request):
        return render(request, 'accommodations/accommodation_search.html')

    def post(self, request):
        Searchterm = request.POST.get("searchterm").title()
        NumTravelers = request.POST.get("numtravelers")

        if not Searchterm and not NumTravelers:
            accommodation_list = Accommodation.published.all()
        elif Searchterm and not NumTravelers:
            accommodation_list = Accommodation.published.filter(
                Q(address__contains=Searchterm) | Q(name__contains=Searchterm))
        elif NumTravelers and not Searchterm:
            accommodation_list = Accommodation.published.filter(room__capacity__gte=NumTravelers)
        elif Searchterm and NumTravelers:
            accommodation_list = Accommodation.published.filter(
                Q(address__contains=Searchterm) | Q(name__contains=Searchterm)).filter(
                room__capacity__gte=NumTravelers)
        Range = request.POST.get("daterange")
        Rangesplit = Range.split(' to ')
        CheckIn = Rangesplit[0]
        CheckOut = Rangesplit[1]
        request.session['checkin'] = CheckIn
        request.session['checkout'] = CheckOut
        accommodation_qs = accommodation_list
        context = {'accommodations': accommodation_qs}
        return render(request, 'accommodations/accommodation_wall.html', context)


@login_required
def book_room(request, accommodation_pk, room_pk):
    FirstDate = request.session['checkin']
    SecDate = request.session['checkout']

    Checkin = datetime.datetime.strptime(FirstDate, "%Y-%m-%d").date()
    Checkout = datetime.datetime.strptime(SecDate, "%Y-%m-%d").date()
    timedeltaSum = Checkout - Checkin

    StayDuration = timedeltaSum.days

    accommodation = Accommodation.published.get(id=accommodation_pk)
    theRoom = Room.objects.get(id=room_pk)

    price = theRoom.type.price
    TotalCost = StayDuration * price

    context = {
        'checkin': Checkin,
        'checkout': Checkout,
        'stayduration': StayDuration,
        'accommodation': accommodation,
        'room': theRoom,
        'price': price,
        'totalcost': TotalCost}
    return render(request, 'accommodations/booking.html', context)


@login_required
def reserve_room(request, accommodation_pk, room_pk, checkin, checkout, totalcost):
    if request.method == 'POST':

        Firstname = request.POST.get('firstname')
        Lastname = request.POST.get('lastname')
        user = request.user
        accommodation = Accommodation.published.get(id=accommodation_pk)
        room = Room.objects.get(id=room_pk)
        cost = totalcost
        new_reservation = Reservation()
        new_reservation.accommodation = accommodation
        new_reservation.room = room
        new_reservation.user = user
        new_reservation.guest_first_name = Firstname
        new_reservation.guest_last_name = Lastname
        new_reservation.CheckIn = checkin
        new_reservation.CheckOut = checkout
        new_reservation.totalPrice = cost
        new_reservation.save()
        # Deletes the session variables.
        del request.session['checkin']
        del request.session['checkout']
        link = reverse('user_bookings')
        return HttpResponseRedirect(link)
    else:
        url = reverse('user_bookings')
        return url


@login_required
def user_bookings(request):
    bookings = Reservation.objects.filter(user=request.user)
    context = {'bookings': bookings}
    return render(request, 'accommodations/mybookings.html', context)


@login_required
def cancel_booking(request, booking_pk):
    booking = Reservation.objects.get(id=booking_pk)
    booking.delete()
    currentuser = request.user
    link = reverse('user_bookings')
    return HttpResponseRedirect(link)


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        booking = Reservation.objects.get(id=self.kwargs['booking_pk'])
        template = get_template('accommodations/invoice.html')
        context = {"booking": booking}
        html = template.render(context)
        pdf = render_to_pdf('accommodations/invoice.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


class AccommodationReviewCreateView(CreateView):
    model = AccommodationReview
    fields = ['comment', 'rating']

    def get_success_url(self):
        accommodation_pk = self.kwargs['id']
        url = reverse('accommodation_detail', args=[accommodation_pk])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.accommodation_id = self.kwargs['id']
        return super(AccommodationReviewCreateView, self).form_valid(form)


class AccommodationReviewUpdateView(UpdateView):
    model = AccommodationReview
    fields = ['comment', 'rating']

    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = AccommodationReview.objects.get(id=review_pk)
        accommodation = review.accommodation
        accommodation_pk = accommodation.id
        url = reverse('accommodation_detail', args=[accommodation_pk])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AccommodationReviewUpdateView, self).form_valid(form)


class AccommodationReviewDeleteView(DeleteView):
    model = AccommodationReview

    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = AccommodationReview.objects.get(id=review_pk)
        accommodation = review.accommodation
        accommodation_pk = accommodation.id
        url = reverse('accommodation_detail', args=[accommodation_pk])
        return url


# #######################################===>END OF ACCOMMODATION MODULE<===##########################################


# ###################################===>BEGINNING OF ROUTE MODULE<===#########################################


class RouteListView(ListView):
    model = Route
    template_name = 'routes/route_list.html'
    context_object_name = 'routes'


class RouteCreateView(CreateView):
    model = Route
    template_name = 'routes/route_create.html'
    fields = ('start_point', 'via', 'end_point', 'route_time', 'price', 'Is_View_on_Web')

    def form_valid(self, form):
        route = form.save(commit=False)
        route.save()
        return redirect('route_list')


class RouteUpdateView(UpdateView):
    model = Route
    template_name = 'routes/update_route.html'
    pk_url_kwarg = 'route_pk'
    fields = ('start_point', 'via', 'end_point', 'route_time', 'price', 'Is_View_on_Web')

    def form_valid(self, form):
        route = form.save(commit=False)
        route.save()
        return redirect('route_list')


@login_required
def save_route_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            routes = Route.objects.all()
            data['html_route_list'] = render_to_string(
                'routes/includes/partial_route_list.html', {
                    'routes': routes
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def route_view(request, route_pk):
    route = get_object_or_404(Route, pk=route_pk)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
    else:
        form = RouteForm(instance=route)
    return save_route_form(request, form, 'routes/includes/partial_bus_view.html')


def route_detail(request, route_pk):
    route = get_object_or_404(Route, pk=route_pk)

    buses = Bus.published.filter(route=route)
    current_user = request.user

    context = {
        'route': route,
        'user': current_user,
        'buses': buses,
    }
    return render(request, 'routes/route_detail.html', context)


@login_required
def route_delete(request, route_pk):
    route = get_object_or_404(Route, pk=route_pk)
    data = dict()
    if request.method == 'POST':
        route.delete()
        data['form_is_valid'] = True
        routes = Route.objects.all()
        data['html_route_list'] = render_to_string('routes/includes/partial_route_list.html', {
            'routes': routes
        })
    else:
        context = {'route': route}
        data['html_form'] = render_to_string('routes/includes/partial_route_delete.html', context, request=request)
    return JsonResponse(data)


class route_search(View):
    def get(self, request):
        return render(request, 'routes/route_search.html')

    def post(self, request):
        Searchterm = request.POST.get("searchterm").title()

        if not Searchterm:
            route_list = Route.published.all()
        elif Searchterm:
            route_list = Route.published.filter(
                Q(start_point__contains=Searchterm) | Q(end_point__contains=Searchterm) | Q(via__contains=Searchterm))
        route_qs = route_list
        context = {'routes': route_qs}
        return render(request, 'routes/route_wall.html', context)


@login_required
def book_bus(request, route_pk, bus_pk):
    route = Route.published.get(id=route_pk)
    theBus = Bus.published.get(id=bus_pk)

    price = theBus.route.price
    TotalCost = price

    context = {
        'route': route,
        'bus': theBus,
        'price': price,
        'totalcost': TotalCost
    }
    return render(request, 'routes/booking.html', context)


@login_required
def reserve_bus(request, route_pk, bus_pk):
    if request.method == 'POST':

        Firstname = request.POST.get('firstname')
        Lastname = request.POST.get('lastname')
        JourneyDate = request.POST.get('travel_date')
        user = request.user
        route = Route.published.get(id=route_pk)
        bus = Bus.published.get(id=bus_pk)
        new_booking = BusReservation()
        new_booking.route = route
        new_booking.bus = bus
        new_booking.user = user
        new_booking.traveller_first_name = Firstname
        new_booking.traveller_last_name = Lastname
        new_booking.travel_date = JourneyDate
        new_booking.save()

        link = reverse('user_bus_bookings')
        return HttpResponseRedirect(link)
    else:
        url = reverse('user_bus_bookings')
        return url


@login_required
def user_bus_bookings(request):
    bookings = BusReservation.objects.filter(user=request.user)
    context = {'bookings': bookings}
    return render(request, 'routes/mybookings.html', context)


@login_required
def cancel_bus_booking(request, booking_pk):
    booking = BusReservation.objects.get(id=booking_pk)
    booking.delete()
    currentuser = request.user
    link = reverse('user_bus_bookings')
    return HttpResponseRedirect(link)


class GenerateBusPDF(View):
    def get(self, request, *args, **kwargs):
        booking = BusReservation.objects.get(id=self.kwargs['booking_pk'])
        template = get_template('routes/invoice.html')
        context = {"booking": booking}
        html = template.render(context)
        pdf = render_to_pdf('routes/invoice.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


class BusReviewCreateView(CreateView):
    model = BusReview
    fields = ['comment', 'rating']

    def get_success_url(self):
        bus_pk = self.kwargs['id']
        url = reverse('bus_detail', args=[bus_pk])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.bus_id = self.kwargs['id']
        return super(BusReviewCreateView, self).form_valid(form)


class BusReviewUpdateView(UpdateView):
    model = BusReview
    fields = ['comment', 'rating']

    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = BusReview.objects.get(id=review_pk)
        bus = review.bus
        bus_pk = bus.id
        url = reverse('bus_detail', args=[bus_pk])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BusReviewUpdateView, self).form_valid(form)


class BusReviewDeleteView(DeleteView):
    model = BusReview

    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = BusReview.objects.get(id=review_pk)
        bus = review.bus
        bus_pk = bus.id
        url = reverse('bus_detail', args=[bus_pk])
        return url


# #######################################===>END OF ROUTE MODULE<===##################################################

# ###################################===>BEGINNING OF BUS MODULE<===#################################################

class BusListView(ListView):
    model = Bus
    template_name = 'buses/bus_list.html'
    context_object_name = 'buses'


class BusCreateView(CreateView):
    model = Bus
    template_name = 'buses/bus_create.html'
    fields = ('number', 'route', 'ac', 'total_seats', 'departure_time', 'image', 'Is_View_on_Web')

    def form_valid(self, form):
        bus = form.save(commit=False)
        bus.save()
        return redirect('bus_list')

    def get_context_data(self, **kwargs):
        context = super(BusCreateView, self).get_context_data(**kwargs)
        context["routes"] = Route.published.all()
        return context


class BusUpdateView(UpdateView):
    model = Bus
    template_name = 'buses/update_bus.html'
    pk_url_kwarg = 'bus_pk'
    fields = ('number', 'route', 'ac', 'total_seats', 'departure_time', 'image', 'Is_View_on_Web')

    def form_valid(self, form):
        bus = form.save(commit=False)
        bus.save()
        return redirect('bus_list')

    def get_context_data(self, **kwargs):
        context = super(BusUpdateView, self).get_context_data(**kwargs)
        context["routes"] = Route.published.all()
        return context


@login_required
def save_bus_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            buses = Bus.objects.all()
            data['html_bus_list'] = render_to_string('buses/includes/partial_bus_list.html', {
                'buses': buses
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def bus_view(request, bus_pk):
    bus = get_object_or_404(Bus, pk=bus_pk)
    if request.method == 'POST':
        form = BusForm(request.POST, instance=bus)
    else:
        form = BusForm(instance=bus)
    return save_bus_form(request, form, 'buses/includes/partial_bus_view.html')


@login_required
def bus_delete(request, bus_pk):
    bus = get_object_or_404(Bus, pk=bus_pk)
    data = dict()
    if request.method == 'POST':
        bus.delete()
        data['form_is_valid'] = True
        buses = Bus.objects.all()
        data['html_bus_list'] = render_to_string('buses/includes/partial_bus_list.html', {
            'buses': buses
        })
    else:
        context = {'bus': bus}
        data['html_form'] = render_to_string('buses/includes/partial_bus_delete.html', context, request=request)
    return JsonResponse(data)


# ###################################===>END OF BUS MODULE<===#####################################################

# ###################################===>BEGINNING OF ROOM MODULE<===#################################################


class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'


def room_create(request):
    accommodations = Accommodation.published.all()
    types = RoomType.objects.all()
    form = RoomForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        room = form.save(commit=False)
        room.save()
        return redirect('room_list')
    context = {
        'form': form,
        'accommodations': accommodations,
        'types': types,
    }
    return render(request, 'rooms/room_create.html', context)


class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'rooms/update_room.html'
    pk_url_kwarg = 'room_pk'
    fields = ('type', 'totalRooms', 'capacity')

    def form_valid(self, form):
        room = form.save(commit=False)
        room.save()
        return redirect('room_list')

    def get_context_data(self, **kwargs):
        context = super(RoomUpdateView, self).get_context_data(**kwargs)
        context["types"] = RoomType.objects.all()
        return context


@login_required
def save_room_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            rooms = Room.objects.all()
            data['html_room_list'] = render_to_string('rooms/includes/partial_room_list.html', {
                'rooms': rooms
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def room_view(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
    else:
        form = RoomForm(instance=room)
    return save_room_form(request, form, 'rooms/includes/partial_room_view.html')


@login_required
def room_delete(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    data = dict()
    if request.method == 'POST':
        room.delete()
        data['form_is_valid'] = True
        rooms = Room.objects.all()
        data['html_room_list'] = render_to_string('rooms/includes/partial_room_list.html', {
            'rooms': rooms
        })
    else:
        context = {'room': room}
        data['html_form'] = render_to_string('rooms/includes/partial_room_delete.html', context, request=request)
    return JsonResponse(data)


# ###################################===>END OF ROOM MODULE<===#####################################################

# ###################################===>BEGINNING OF TYPE MODULE<===#################################################


class TypeListView(ListView):
    model = RoomType
    template_name = 'types/type_list.html'
    context_object_name = 'types'


class TypeCreateView(CreateView):
    model = RoomType
    template_name = 'types/type_create.html'
    fields = ('accommodation', 'price', 'description', 'image')

    def form_valid(self, form):
        type = form.save(commit=False)
        type.save()
        return redirect('bus_list')

    def get_context_data(self, **kwargs):
        context = super(TypeCreateView, self).get_context_data(**kwargs)
        context["accommodations"] = Accommodation.published.all()
        return context


class TypeUpdateView(UpdateView):
    model = RoomType
    template_name = 'types/update_type.html'
    pk_url_kwarg = 'type_pk'
    fields = ('accommodation', 'price', 'description', 'image')

    def form_valid(self, form):
        type = form.save(commit=False)
        type.save()
        return redirect('type_list')

    def get_context_data(self, **kwargs):
        context = super(TypeUpdateView, self).get_context_data(**kwargs)
        context["accommodations"] = Accommodation.published.all()
        return context


@login_required
def save_type_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            types = RoomType.objects.all()
            data['html_type_list'] = render_to_string('types/includes/partial_type_list.html', {
                'types': types
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def type_view(request, type_pk):
    type = get_object_or_404(RoomType, pk=type_pk)
    if request.method == 'POST':
        form = RoomTypeForm(request.POST, instance=type)
    else:
        form = RoomTypeForm(instance=type)
    return save_type_form(request, form, 'types/includes/partial_type_view.html')


@login_required
def type_delete(request, type_pk):
    type = get_object_or_404(RoomType, pk=type_pk)
    data = dict()
    if request.method == 'POST':
        type.delete()
        data['form_is_valid'] = True
        types = RoomType.objects.all()
        data['html_type_list'] = render_to_string('types/includes/partial_type_list.html', {
            'types': types
        })
    else:
        context = {'type': type}
        data['html_form'] = render_to_string('types/includes/partial_type_delete.html', context, request=request)
    return JsonResponse(data)


# ###################################===>END OF TYPE MODULE<===#####################################################

# ###################################===>BEGINNING OF TAXI MODULE<===#################################################

class TaxiListView(ListView):
    model = Taxi
    template_name = 'taxis/taxi_list.html'
    context_object_name = 'taxis'


def taxi_wall(request):
    taxis = Taxi.published.all()
    return render(request, 'taxis/taxis_wall.html', {'taxis': taxis})


class TaxiCreateView(CreateView):
    model = Taxi
    template_name = 'taxis/taxi_create.html'
    fields = ('driver', 'number', 'ac', 'total_seats', 'taxi_type', 'taxi_info', 'image', 'fare_ratio', 'source')

    def form_valid(self, form):
        taxi = form.save(commit=False)
        taxi.save()
        return redirect('taxi_list')

    def get_context_data(self, **kwargs):
        context = super(TaxiCreateView, self).get_context_data(**kwargs)
        context["drivers"] = Driver.published.all()
        return context


class TaxiUpdateView(UpdateView):
    model = Taxi
    template_name = 'taxis/update_taxi.html'
    pk_url_kwarg = 'taxi_pk'
    fields = ('driver', 'number', 'ac', 'total_seats', 'taxi_type', 'taxi_info', 'image', 'fare_ratio', 'source',
              'Is_View_on_Web')

    def form_valid(self, form):
        taxi = form.save(commit=False)
        taxi.save()
        return redirect('taxi_list')

    def get_context_data(self, **kwargs):
        context = super(TaxiUpdateView, self).get_context_data(**kwargs)
        context["drivers"] = Driver.published.all()
        return context


@login_required
def save_taxi_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            taxis = Taxi.objects.all()
            data['html_taxi_list'] = render_to_string('taxis/includes/partial_taxi_list.html', {
                'taxis': taxis
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def taxi_view(request, taxi_pk):
    taxi = get_object_or_404(Taxi, pk=taxi_pk)
    if request.method == 'POST':
        form = TaxiForm(request.POST, instance=taxi)
    else:
        form = TaxiForm(instance=taxi)
    return save_taxi_form(request, form, 'taxis/includes/partial_taxi_view.html')


@login_required
def taxi_delete(request, taxi_pk):
    taxi = get_object_or_404(Taxi, pk=taxi_pk)
    data = dict()
    if request.method == 'POST':
        taxi.delete()
        data['form_is_valid'] = True
        taxis = Taxi.objects.all()
        data['html_taxi_list'] = render_to_string('taxis/includes/partial_taxi_list.html', {
            'taxis': taxis
        })
    else:
        context = {'taxi': taxi}
        data['html_form'] = render_to_string('taxis/includes/partial_taxi_delete.html', context, request=request)
    return JsonResponse(data)


@login_required
def book_taxi(request, taxi_pk):
    taxi = get_object_or_404(Taxi, pk=taxi_pk)
    price = taxi.fare_ratio

    context = {
        'price': price,
        'taxi': taxi
    }
    return render(request, 'taxis/booking.html', context)


@login_required
def reserve_taxi_slot(request, taxi_pk):
    if request.method == 'POST':
        Firstname = request.POST.get('firstname')
        Lastname = request.POST.get('lastname')
        TravelDate = request.POST.get('travel_date')
        TravelTime = request.POST.get('travel_time')
        user = request.user
        taxi = Taxi.published.get(id=taxi_pk)
        new_booking = TaxiBooking()
        new_booking.taxi = taxi
        new_booking.user = user
        new_booking.traveller_first_name = Firstname
        new_booking.traveller_last_name = Lastname
        new_booking.travel_date = TravelDate
        new_booking.travel_time = TravelTime
        new_booking.save()
        link = reverse('user_taxi_bookings')
        return HttpResponseRedirect(link)
    else:
        url = reverse('user_taxi_bookings')
        return url


@login_required
def user_taxi_bookings(request):
    bookings = TaxiBooking.objects.filter(user=request.user)
    context = {'bookings': bookings}
    return render(request, 'taxis/mybookings.html', context)


@login_required
def cancel_taxi_booking(request, taxi_pk):
    booking = TaxiBooking.objects.get(id=taxi_pk)
    booking.delete()
    currentuser = request.user
    link = reverse('user_taxi_bookings')
    return HttpResponseRedirect(link)


class GenerateTaxiPDF(View):
    def get(self, request, *args, **kwargs):
        booking = TaxiBooking.objects.get(id=self.kwargs['taxi_pk'])
        template = get_template('taxis/invoice.html')
        context = {"booking": booking}
        html = template.render(context)
        pdf = render_to_pdf('taxis/invoice.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


class TaxiReviewCreateView(CreateView):
    model = TaxiReview
    fields = ['comment', 'rating']

    def get_success_url(self):
        taxi_pk = self.kwargs['id']
        url = reverse('taxi_detail', args=[taxi_pk])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.taxi_id = self.kwargs['id']
        return super(TaxiReviewCreateView, self).form_valid(form)


class TaxiReviewUpdateView(UpdateView):
    model = TaxiReview
    fields = ['comment', 'rating']

    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = TaxiReview.objects.get(id=review_pk)
        taxi = review.taxi
        taxi_pk = taxi.id
        url = reverse('taxi_detail', args=[taxi_pk])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaxiReviewUpdateView, self).form_valid(form)


class TaxiReviewDeleteView(DeleteView):
    model = TaxiReview

    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = TaxiReview.objects.get(id=review_pk)
        taxi = review.taxi
        taxi_pk = taxi.id
        url = reverse('taxi_detail', args=[taxi_pk])
        return url


# #######################################===>END OF TAXI MODULE<===##################################################

# ###################################===>BEGINNING OF CAB MODULE<===#################################################


class CabListView(ListView):
    model = AirportTaxi
    template_name = 'cabs/cab_list.html'
    context_object_name = 'cabs'


def cab_wall(request):
    cabs = AirportTaxi.published.all()
    return render(request, 'cabs/cabs_wall.html', {'cabs': cabs})


class CabCreateView(CreateView):
    model = AirportTaxi
    template_name = 'cabs/cab_create.html'
    fields = ('driver', 'number', 'ac', 'total_seats', 'taxi_type', 'taxi_info', 'image', 'fare_ratio', 'source')

    def form_valid(self, form):
        cab = form.save(commit=False)
        cab.save()
        return redirect('cab_list')

    def get_context_data(self, **kwargs):
        context = super(CabCreateView, self).get_context_data(**kwargs)
        context["drivers"] = Driver.published.all()
        return context


class CabUpdateView(UpdateView):
    model = AirportTaxi
    template_name = 'cabs/update_cab.html'
    pk_url_kwarg = 'cab_pk'
    fields = ('driver', 'number', 'ac', 'total_seats', 'taxi_type', 'taxi_info', 'image', 'fare_ratio', 'source')

    def form_valid(self, form):
        cab = form.save(commit=False)
        cab.save()
        return redirect('cab_list')

    def get_context_data(self, **kwargs):
        context = super(CabUpdateView, self).get_context_data(**kwargs)
        context["drivers"] = Driver.published.all()
        return context


@login_required
def save_cab_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            cabs = AirportTaxi.objects.all()
            data['html_cab_list'] = render_to_string('cabs/includes/partial_cab_list.html', {
                'cabs': cabs
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def cab_view(request, cab_pk):
    cab = get_object_or_404(AirportTaxi, pk=cab_pk)
    if request.method == 'POST':
        form = AirportTaxiForm(request.POST, instance=cab)
    else:
        form = AirportTaxiForm(instance=cab)
    return save_cab_form(request, form, 'cabs/includes/partial_cab_view.html')


@login_required
def cab_delete(request, cab_pk):
    cab = get_object_or_404(AirportTaxi, pk=cab_pk)
    data = dict()
    if request.method == 'POST':
        cab.delete()
        data['form_is_valid'] = True
        cabs = AirportTaxi.objects.all()
        data['html_cab_list'] = render_to_string('cabs/includes/partial_cab_list.html', {
            'cabs': cabs
        })
    else:
        context = {'cab': cab}
        data['html_form'] = render_to_string('cabs/includes/partial_cab_delete.html', context, request=request)
    return JsonResponse(data)


@login_required
def book_cab(request, cab_pk):
    cab = get_object_or_404(AirportTaxi, pk=cab_pk)
    price = cab.fare_ratio

    context = {
        'price': price,
        'cab': cab
    }
    return render(request, 'cabs/booking.html', context)


@login_required
def reserve_cab_slot(request, cab_pk):
    if request.method == 'POST':
        Firstname = request.POST.get('firstname')
        Lastname = request.POST.get('lastname')
        TravelDate = request.POST.get('travel_date')
        TravelTime = request.POST.get('travel_time')
        Destination = request.POST.get('destination')
        user = request.user
        cab = AirportTaxi.published.get(id=cab_pk)
        new_booking = AirportTaxiBooking()
        new_booking.cab = cab
        new_booking.user = user
        new_booking.traveller_first_name = Firstname
        new_booking.traveller_last_name = Lastname
        new_booking.travel_date = TravelDate
        new_booking.travel_time = TravelTime
        new_booking.destination = Destination
        new_booking.save()
        link = reverse('user_cab_bookings')
        return HttpResponseRedirect(link)
    else:
        url = reverse('user_cab_bookings')
        return url


@login_required
def user_cab_bookings(request):
    bookings = AirportTaxiBooking.objects.filter(user=request.user)
    context = {'bookings': bookings}
    return render(request, 'cabs/mybookings.html', context)


@login_required
def cancel_cab_booking(request, cab_pk):
    booking = AirportTaxiBooking.objects.get(id=cab_pk)
    booking.delete()
    currentuser = request.user
    link = reverse('user_cab_bookings')
    return HttpResponseRedirect(link)


class GenerateCabPDF(View):
    def get(self, request, *args, **kwargs):
        booking = AirportTaxiBooking.objects.get(id=self.kwargs['cab_pk'])
        template = get_template('cabs/invoice.html')
        context = {"booking": booking}
        html = template.render(context)
        pdf = render_to_pdf('cabs/invoice.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


# #######################################===>END OF CAB MODULE<===##################################################

# ###################################===>BEGINNING OF DRIVER MODULE<===#################################################


class DriverListView(ListView):
    model = Driver
    template_name = 'drivers/driver_list.html'
    context_object_name = 'drivers'


def driver_wall(request):
    drivers = Driver.objects.all()
    return render(request, 'drivers/drivers_wall.html', {'drivers': drivers})


class DriverCreateView(CreateView):
    model = Driver
    template_name = 'drivers/driver_create.html'
    fields = ('name', 'contact', 'address', 'image', 'rating', 'Is_View_on_Web')

    def form_valid(self, form):
        driver = form.save(commit=False)
        driver.save()
        return redirect('driver_list')


class DriverUpdateView(UpdateView):
    model = Driver
    template_name = 'drivers/update_driver.html'
    pk_url_kwarg = 'driver_pk'
    fields = ('name', 'contact', 'address', 'image', 'rating', 'Is_View_on_Web')

    def form_valid(self, form):
        driver = form.save(commit=False)
        driver.save()
        return redirect('driver_list')


@login_required
def save_driver_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            drivers = Driver.objects.all()
            data['html_driver_list'] = render_to_string('drivers/includes/partial_driver_list.html', {
                'drivers': drivers
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
def driver_view(request, driver_pk):
    driver = get_object_or_404(Driver, pk=driver_pk)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
    else:
        form = DriverForm(instance=driver)
    return save_driver_form(request, form, 'drivers/includes/partial_driver_view.html')


def driver_detail(request, driver_pk):
    driver = get_object_or_404(Driver, pk=driver_pk)
    more_drivers = Driver.published.order_by('-from_date')[:5]
    context = {
        'driver': driver,
        'more_drivers': more_drivers
    }
    return render(request, 'drivers/driver_detail.html', context)


@login_required
def driver_delete(request, driver_pk):
    driver = get_object_or_404(Driver, pk=driver_pk)
    data = dict()
    if request.method == 'POST':
        driver.delete()
        data['form_is_valid'] = True
        drivers = Driver.objects.all()
        data['html_driver_list'] = render_to_string('drivers/includes/partial_driver_list.html', {
            'drivers': drivers
        })
    else:
        context = {'driver': driver}
        data['html_form'] = render_to_string('drivers/includes/partial_driver_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


class CabReviewCreateView(CreateView):
    model = CabReview
    fields = ['comment', 'rating']

    def get_success_url(self):
        cab_pk = self.kwargs['id']
        url = reverse('cab_detail', args=[cab_pk])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.cab_id = self.kwargs['id']
        return super(CabReviewCreateView, self).form_valid(form)


class CabReviewUpdateView(UpdateView):
    model = CabReview
    fields = ['comment', 'rating']

    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = CabReview.objects.get(id=review_pk)
        cab = review.cab
        cab_pk = cab.id
        url = reverse('cab_detail', args=[cab_pk])
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CabReviewUpdateView, self).form_valid(form)


class CabReviewDeleteView(DeleteView):
    model = CabReview

    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = CabReview.objects.get(id=review_pk)
        cab = review.cab
        cab_pk = cab.id
        url = reverse('cab_detail', args=[cab_pk])
        return url


# #######################################===>END OF DRIVER MODULE<===##################################################

class AccommodationBookingListView(ListView):
    model = Reservation
    template_name = 'bookings/room_list.html'
    context_object_name = 'rooms'


class BusBookingListView(ListView):
    model = BusReservation
    template_name = 'bookings/bus_list.html'
    context_object_name = 'buses'


class TripBookingListView(ListView):
    model = TripBooking
    template_name = 'bookings/trip_list.html'
    context_object_name = 'trips'


class CabBookingListView(ListView):
    model = AirportTaxiBooking
    template_name = 'bookings/cab_list.html'
    context_object_name = 'cabs'


class TaxiBookingListView(ListView):
    model = TaxiBooking
    template_name = 'bookings/taxi_list.html'
    context_object_name = 'taxis'
