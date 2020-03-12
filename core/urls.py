from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls import url
from registration.backends.simple.views import RegistrationView


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/zuulatravels/'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookings.urls')),
    url(r'^social/', include('allauth.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
