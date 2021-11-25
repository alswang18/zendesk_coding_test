from django.urls import path

from .views import ticket_list

urlpatterns = [path("", ticket_list, name="ticket_list")]
