import os
import traceback
from math import ceil

import requests

PER_PAGE = 25


def get_group_name(group_id):
    ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
    ZENDESK_USER = os.environ.get("ZENDESK_USER")
    ZENDESK_URL = os.environ.get("ZENDESK_URL") + f"/api/v2/groups/{group_id}"
    response = requests.get(ZENDESK_URL, auth=(ZENDESK_USER, ZENDESK_PASSWORD))
    try:
        resp = response.json()
        return resp["group"]["name"]
    except Exception:
        return None


def get_user_name(user_id):
    ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
    ZENDESK_USER = os.environ.get("ZENDESK_USER")
    ZENDESK_URL = os.environ.get("ZENDESK_URL") + f"/api/v2/users/{user_id}"
    response = requests.get(ZENDESK_URL, auth=(ZENDESK_USER, ZENDESK_PASSWORD))
    try:
        resp = response.json()
        return resp["user"]["name"]
    except Exception:
        return None


def ticket_count():
    ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
    ZENDESK_URL = os.environ.get("ZENDESK_URL") + "/api/v2/tickets/count.json"
    ZENDESK_USER = os.environ.get("ZENDESK_USER")
    response = requests.get(ZENDESK_URL, auth=(ZENDESK_USER, ZENDESK_PASSWORD)).json()
    return int(response["count"]["value"])


def create_ticket_list_context(page=1):
    ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
    # bounds the current page to 1-ceil(ticket_count/25)
    current_page = min(ceil(ticket_count() / PER_PAGE), max(int(page), 1))
    ZENDESK_URL = (
        os.environ.get("ZENDESK_URL")
        + "/api/v2/tickets.json?per_page="
        + str(PER_PAGE)
        + "&page="
        + str(current_page)
    )
    ZENDESK_USER = os.environ.get("ZENDESK_USER")

    response = requests.get(ZENDESK_URL, auth=(ZENDESK_USER, ZENDESK_PASSWORD))

    context = dict()
    context["error"] = False
    if response.status_code != 200:
        context["error"] = True
        context[
            "error_message"
        ] = f"""
                😅 This GET request came back with code {response.status_code}.
                That means your tickets may not be available.
                Try again in a few minutes or contact asw15@sfu.ca for assistance.
            """
        return context
    try:
        resp = response.json()
        context["tickets"] = resp["tickets"]
        context["has_less"] = page > 1
        context["prev_page"] = page - 1
        context["has_more"] = ceil(ticket_count() / 2) > page
        context["next_page"] = page + 1
        context["max"] = ceil(ticket_count() / 2)
    except Exception:
        context["error"] = True
        context[
            "error_message"
        ] = f"""
                😅 Something unexpected went wrong. Here's the 
                error stack {traceback.format_exc()}. Try again in a few minutes or contact 
                asw15@sfu.ca for assistance.
            """
    return context
