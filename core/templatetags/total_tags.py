from django import template
from django.db.models import Sum

from ..models import *

register = template.Library()


@register.simple_tag
def total_drivers():
    return Driver.published.all().count()


@register.simple_tag
def total_apartment_bookings():
    return Room.objects.all().count()


@register.simple_tag
def total_trip_bookings():
    return TripBooking.objects.all().count()


@register.simple_tag
def total_bus_bookings():
    return BusReservation.objects.all().count()


@register.simple_tag
def total_hire_bookings():
    return TaxiBooking.objects.all().count()


@register.simple_tag
def total_cab_bookings():
    return AirportTaxiBooking.objects.all().count()


@register.simple_tag
def total_client_bookings():
    return User.objects.all().count()
#
# @register.simple_tag
# def total_accountants():
#     return Employee.objects.all().count()
#
#
# @register.simple_tag
# def total_administrators():
#     return Employee.objects.all().count()
#
#
# @register.simple_tag
# def total_librarians():
#     return Employee.objects.all().count()
