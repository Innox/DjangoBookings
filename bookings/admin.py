from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from bookings.models import *

# Registers the Hotels and review models on the Django Admin page
admin.site.register(Slider)
admin.site.register(About)
admin.site.register(Event)
admin.site.register(News)
admin.site.register(Accommodation)
admin.site.register(Reservation)
admin.site.register(BusReservation)
admin.site.register(TripBooking)
admin.site.register(Route)
admin.site.register(Bus)
admin.site.register(Driver)
admin.site.register(AirportTaxi)
admin.site.register(Taxi)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'price')


class BookingAdmin(admin.ModelAdmin):
    list_display = ('Room', 'RoomNumber', 'User', 'Checkin', 'Checkout', 'Bill')
    list_display_links = None

    def has_add_permission(self, request):
        return False


class UserControlAdmin(UserAdmin):
    list_display_links = None

    def has_add_permission(self, request):
        return False


class ImageAdmin(admin.ModelAdmin):
    list_display = ('Image', 'RoomType')


# admin.site.register(Profile,ProfileAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType)
admin.site.unregister(User)
admin.site.register(User, UserControlAdmin)

admin.site.site_header = 'Bookings'
admin.site.site_title = 'Bookings'


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'phone', 'date',)
    search_fields = ('name', 'email', 'phone',)
    date_hierarchy = 'date'


admin.site.register(Feedback, FeedbackAdmin)
