from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

ROLE_CHOICES = (
    ('All', 'All'),
    ('Family', 'Family'),
    ('Singles', 'Singles'),
    ('Couples', 'Couples'),
    ('Children', 'Children'),
)

OPTIONS = (('Yes', 'Yes'),
           ('No', 'No'))

TAXI_TYPES = (
    ('SUV', 'SUV'),
    ('TRUCK', 'Truck'),
    ('SEDAN', 'Sedan'),
    ('VAN', 'Van'),
    ('WAGON', 'Wagon'),
    ('CONVERTIBLE', 'Convertible'),
    ('SPORTS', 'Sports'),
    ('DIESEL', 'Diesel'),
    ('LUXURY', 'Luxury'),
    ('HATCHBACK', 'Hatchback'),
    ('OTHER', 'Other'),
)


class Slider(models.Model):
    slider_image = models.ImageField(_('Slider Image'), upload_to='sliders/')
    image_title = models.CharField(_('Image Title'), max_length=100)
    modified = models.DateTimeField(verbose_name=_('Modified'), auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.image_title


class About(models.Model):
    about_image = models.ImageField(_('About Image'), upload_to='about/', null=True, blank=False)
    about = models.TextField(_('About School'), max_length=500)
    modified = models.DateTimeField(verbose_name=_('Modified'), auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        verbose_name = _("About")
        verbose_name_plural = _("About")

    def __str__(self):
        return self.about

    def get_absolute_url(self):
        return reverse('about_detail', args=[self.pk])


class PublishedStatusManager(models.Manager):
    def get_queryset(self):
        return super(PublishedStatusManager, self).get_queryset().filter(Is_View_on_Web='Yes')


class News(models.Model):
    news_title = models.CharField(_('News Title'), max_length=100)
    date = models.DateField(_('Date'), auto_now_add=True)
    image = models.ImageField(_('Image'), upload_to='images/', null=True, blank=False)
    news = models.TextField(_('News'), blank=True)
    Is_View_on_Web = models.CharField(_('Is View On Web?'), max_length=20, default='Yes', choices=OPTIONS)
    author = models.ForeignKey(User, verbose_name=_('Author'), on_delete=models.CASCADE, related_name='news',
                               blank=True)

    objects = models.Manager()
    published = PublishedStatusManager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ('-date',)

    def __str__(self):
        return self.news_title

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.pk])


class Event(models.Model):
    event_title = models.CharField(_('Trip Title'), max_length=100)
    event_for = models.CharField(verbose_name=_('Trip For'), max_length=100, choices=ROLE_CHOICES)
    event_place = models.CharField(_('Trip Place'), max_length=100)
    from_date = models.DateField(_('From Date'))
    to_date = models.DateField(_('To Date'))
    image = models.ImageField(_('Image'), upload_to='images/', null=True, blank=True)
    price = models.PositiveIntegerField()
    offer = models.BooleanField(default=False)
    note = models.TextField(_('Note'), blank=True, null=True)
    Is_View_on_Web = models.CharField(_('Is View On Web?'), max_length=20, default='Yes', choices=OPTIONS, blank=True,
                                      null=True)

    objects = models.Manager()
    published = PublishedStatusManager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ('from_date',)

    def __str__(self):
        return self.event_title

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.pk])


class EventReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Trip Review'

    def __str__(self):
        return self.comment


class TripBooking(models.Model):
    trip = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tourist_first_name = models.CharField(max_length=255)
    tourist_last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Trip'

    def __str__(self):
        return self.tourist_last_name


class ActiveGuestManager(models.Manager):
    def get_queryset(self):
        return super(ActiveGuestManager, self).get_queryset().filter(Is_View_on_Web='Yes')


class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True, unique=True)
    image = models.ImageField(_('Image'), upload_to='images/', null=True, blank=True)
    lowest_charge = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    note = models.CharField(max_length=300, null=True, blank=True)
    Is_View_on_Web = models.CharField(_('Is View On Web?'), max_length=20, default='Yes', choices=OPTIONS, blank=True,
                                      null=True)

    published = ActiveGuestManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('accommodation_detail', args=[self.pk])


class AccommodationReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Hotel Reviews'

    def __str__(self):
        return self.comment


class RoomType(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, verbose_name='Hotel')
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=None)
    description = models.CharField(max_length=200, default=None)
    airConditioning = models.BooleanField(default=False, verbose_name='Air Conditioning')
    wifi = models.BooleanField(default=False, verbose_name='WiFi')
    roomService = models.BooleanField(default=False, verbose_name='Room Service')
    freeBreakfast = models.BooleanField(default=False, verbose_name='Free Breakfast')
    minibar = models.BooleanField(default=False, verbose_name='Mini Bar')
    laundaryService = models.BooleanField(default=False, verbose_name='Laundary Service')
    poolFacility = models.BooleanField(default=False, verbose_name='Pool Facility')
    image = models.ImageField(_('Room Type Image'), upload_to='RoomTypes/', null=True, blank=True)

    def __str__(self):
        return self.description


class Room(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, verbose_name='Hotel')
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='Room Type', null=True, blank=True)
    totalRooms = models.CharField(max_length=255)
    View = models.BooleanField(default=True)
    capacity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def price(self):
        return self.type.price


class Reservation(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_first_name = models.CharField(max_length=255)
    guest_last_name = models.CharField(max_length=255)
    CheckIn = models.DateField()
    CheckOut = models.DateField()
    totalPrice = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Reservation'

    def __str__(self):
        return self.guest_last_name


class ActiveRouteManager(models.Manager):
    def get_queryset(self):
        return super(ActiveRouteManager, self).get_queryset().filter(Is_View_on_Web='Yes')


class Route(models.Model):
    start_point = models.CharField(max_length=300)
    via = models.CharField(max_length=300)
    end_point = models.CharField(max_length=300)
    route_time = models.CharField(max_length=100, null=True, blank=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=None)
    Is_View_on_Web = models.CharField(_('Is View On Web?'), max_length=20, default='Yes', choices=OPTIONS, blank=True,
                                      null=True)

    @property
    def complete_route(self):
        return str(self.start_point) + " - " + str(self.via) + " - " + str(self.end_point)

    published = ActiveRouteManager()

    def __str__(self):
        return self.start_point + "-" + self.end_point


class ActiveBusManager(models.Manager):
    def get_queryset(self):
        return super(ActiveBusManager, self).get_queryset().filter(Is_View_on_Web='Yes')


class Bus(models.Model):
    number = models.CharField(max_length=40)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    ac = models.BooleanField(default=False)
    total_seats = models.IntegerField(default='56')
    departure_time = models.TimeField()
    image = models.ImageField(upload_to="bus", max_length=100, null=True)
    Is_View_on_Web = models.CharField(_('Is View On Web?'), max_length=20, default='Yes', choices=OPTIONS, blank=True,
                                      null=True)

    published = ActiveBusManager()

    def __str__(self):
        return self.number


class BusReservation(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    traveller_first_name = models.CharField(max_length=255)
    traveller_last_name = models.CharField(max_length=255)
    travel_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Bus Reservations'

    def __str__(self):
        return self.traveller_last_name


class BusReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Bus Reviews'

    def __str__(self):
        return self.comment


class ActiveDriverManager(models.Manager):
    def get_queryset(self):
        return super(ActiveDriverManager, self).get_queryset().filter(Is_View_on_Web='Yes')


class Driver(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=16)
    address = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to="profile", null=True)
    rating = models.CharField(max_length=100, blank=True, null=True)
    Is_View_on_Web = models.CharField(_('Is View On Web?'), max_length=20, default='Yes', choices=OPTIONS, blank=True,
                                      null=True)

    published = ActiveDriverManager()

    def __str__(self):
        return self.name


class ActiveTaxiManager(models.Manager):
    def get_queryset(self):
        return super(ActiveTaxiManager, self).get_queryset().filter(Is_View_on_Web='Yes')


class Taxi(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    number = models.CharField(max_length=40)
    ac = models.BooleanField(default=False)
    total_seats = models.IntegerField(default='4')
    taxi_type = models.CharField(max_length=20, choices=TAXI_TYPES)
    taxi_info = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='taxi', null=True)
    fare_ratio = models.IntegerField(default=10)
    source = models.CharField(max_length=40)
    Is_View_on_Web = models.CharField(_('Is View On Web?'), max_length=20, default='Yes', choices=OPTIONS, blank=True,
                                      null=True)

    published = ActiveTaxiManager()

    def __str__(self):
        return self.number


class TaxiBooking(models.Model):
    taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    traveller_first_name = models.CharField(max_length=255)
    traveller_last_name = models.CharField(max_length=255)
    travel_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    travel_time = models.TimeField()

    class Meta:
        verbose_name_plural = 'Special Hire Reservations'

    def __str__(self):
        return self.traveller_last_name


class TaxiReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Hotel Review'

    def __str__(self):
        return self.comment


class ActiveCabManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCabManager, self).get_queryset().filter(Is_View_on_Web='Yes')


class AirportTaxi(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    number = models.CharField(max_length=40)
    ac = models.BooleanField(default=False)
    total_seats = models.IntegerField(default='4')
    taxi_type = models.CharField(max_length=20, choices=TAXI_TYPES)
    taxi_info = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='taxi', null=True)
    fare_ratio = models.IntegerField(default=10)
    source = models.CharField(max_length=40)
    Is_View_on_Web = models.CharField(_('Is View On Web?'), max_length=20, default='Yes', choices=OPTIONS, blank=True,
                                      null=True)

    published = ActiveCabManager()

    def __str__(self):
        return self.number


class AirportTaxiBooking(models.Model):
    cab = models.ForeignKey(AirportTaxi, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    traveller_first_name = models.CharField(max_length=255)
    traveller_last_name = models.CharField(max_length=255)
    travel_date = models.DateField()
    destination = models.CharField(max_length=40)
    travel_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Airport Taxi Reservations'

    def __str__(self):
        return self.traveller_last_name


class CabReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cab = models.ForeignKey(AirportTaxi, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Hotel Review'

    def __str__(self):
        return self.comment


class Feedback(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the sender")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Feedback"

    def __str__(self):
        return self.name + "-" + self.email
