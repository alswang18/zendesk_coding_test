import os
import traceback
import requests
from django.shortcuts import render
import datetime
from math import ceil
from .utils import create_ticket_list_context, get_group_name, get_user_name, PER_PAGE


# detail-type view
def ticket(request, ticket_id):
    ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
    ZENDESK_USER = os.environ.get("ZENDESK_USER")
    ZENDESK_URL = os.environ.get("ZENDESK_URL") + f"/api/v2/tickets/{ticket_id}"
    response = requests.get(ZENDESK_URL, auth=(ZENDESK_USER, ZENDESK_PASSWORD))
    context = dict()
    context["error"] = False
    if response.status_code == 404:
        context["error"] = True
        context[
            "error_message"
        ] = """
                😅 This ticket does not exist.
                If you think this is wrong, contact asw15@sfu.ca for assistance.
            """
        return render(request, "ticket.html", context)
    if response.status_code != 200:
        context["error"] = True
        context[
            "error_message"
        ] = f"""
                😅 This GET request came back with code {response.status_code}.
                That means your tickets may not be available.
                Try again in a few minutes or contact asw15@sfu.ca for assistance.
            """
        return render(request, "ticket.html", context)
    try:
        resp = response.json()
        context["ticket"] = resp["ticket"]

        context["ticket"]["group_name"] = get_group_name(resp["ticket"]["group_id"])
        context["ticket"]["requester_name"] = get_user_name(
            resp["ticket"]["requester_id"]
        )
        context["ticket"]["updated_at"] =  datetime.datetime.strptime(context["ticket"]["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
        context["ticket"]["created_at"] =  datetime.datetime.strptime(context["ticket"]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        context["back_value"] = request.GET.get("page", 1)
    except Exception:
        context["error"] = True
        context[
            "error_message"
        ] = f"""
                😅 Something unexpected went wrong. Here's the 
                error stack {traceback.format_exc()}. Try again in a few minutes or contact 
                asw15@sfu.ca for assistance.
            """
    return render(request, "ticket.html", context)


# list-type view
def ticket_list(request):
    page = int(request.GET.get("page", 1))
    return render(request, "ticket_list.html", create_ticket_list_context(page))
