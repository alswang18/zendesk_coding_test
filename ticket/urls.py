from django.urls import path

from .views import ticket, ticket_list

urlpatterns = [
    path("", ticket_list, name="ticket_list"),
    path("ticket/<int:ticket_id>", ticket, name="ticket"),
]
