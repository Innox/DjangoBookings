from allauth.account.forms import SignupForm
from django import forms

from .models import *


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ('slider_image', 'image_title')


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ('about', 'about_image')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('news_title', 'image', 'news', 'Is_View_on_Web')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_title', 'event_for', 'price', 'event_place', 'from_date', 'to_date', 'image', 'note',
                  'Is_View_on_Web')


class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ('name', 'code', 'image', 'lowest_charge', 'address')


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('accommodation', 'type', 'totalRooms', 'capacity')


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ('accommodation', 'price', 'description', 'image')


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ('start_point', 'via', 'end_point', 'route_time', 'price', 'Is_View_on_Web')


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ('number', 'route', 'ac', 'total_seats', 'departure_time', 'image', 'Is_View_on_Web')


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('name', 'contact', 'address', 'image', 'rating', 'Is_View_on_Web')


class TaxiForm(forms.ModelForm):
    class Meta:
        model = Taxi
        fields = ('driver', 'number', 'ac', 'total_seats', 'taxi_type', 'taxi_info', 'image', 'fare_ratio', 'source',
                  'Is_View_on_Web')


class AirportTaxiForm(forms.ModelForm):
    class Meta:
        model = AirportTaxi
        fields = ('driver', 'number', 'ac', 'total_seats', 'taxi_type', 'taxi_info', 'image', 'fare_ratio', 'source',
                  'Is_View_on_Web')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
