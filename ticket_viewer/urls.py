from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [path("", include("ticket.urls"), name="ticket-list")]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document=settings.STATIC_ROOT)
