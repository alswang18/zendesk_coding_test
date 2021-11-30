from django.shortcuts import render

from .utils import create_ticket_detail_context, create_ticket_list_context


# detail-type view
def ticket(request, ticket_id):
    page = int(request.GET.get("page", 1))
    return render(request, "ticket.html", create_ticket_detail_context(page, ticket_id))


# list-type view
def ticket_list(request):
    page = int(request.GET.get("page", 1))
    return render(request, "ticket_list.html", create_ticket_list_context(page))
