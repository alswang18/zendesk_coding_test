import logging
import os
import requests
from django.shortcuts import render

# list-type view
def ticket_list(request):
    page_num = request.GET.get("page", "1")
    return render(request, "ticket_list.html", create_ticket_list_context(page_num))

def create_ticket_list_context(page_num):
    ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
    ZENDESK_URL = os.environ.get("ZENDESK_URL")
    ZENDESK_USER = os.environ.get("ZENDESK_USER")

    response = requests.get(
        ZENDESK_URL + "?page=" + str(page_num), auth=(ZENDESK_USER, ZENDESK_PASSWORD)
    )

    context = dict()
    context["error"] = False
    if response.status_code != 200:
        context["error"] = True
        context[
            "error_message"
        ] = f"""
                😅 This GET request came back with code {response.status_code}.\n
                That means your tickets may not be available.\n
                Try again in a few minutes or contact asw15@sfu.ca for assistance.
            """

    try:
        resp = response.json()
        context["tickets"] = resp["tickets"]

    except Exception as err:
        context["error"] = True
        context[
            "error_message"
        ] = f"""
                😅 Something unexpected went wrong. Here's the 
                error stack {err}.\nTry again in a few minutes or contact 
                asw15@sfu.ca for assistance.
            """
    return context