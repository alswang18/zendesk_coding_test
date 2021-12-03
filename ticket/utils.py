import datetime
import os
import traceback
from math import ceil
import requests

# offset per paginated request
PER_PAGE = 25

def get_group_name(group_id):
    try:
        ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
        ZENDESK_USER = os.environ.get("ZENDESK_USER")
        ZENDESK_URL = os.environ.get("ZENDESK_URL") + f"/api/v2/groups/{group_id}"
        response = requests.get(ZENDESK_URL, auth=(ZENDESK_USER, ZENDESK_PASSWORD))
        resp = response.json()
        return resp["group"]["name"]
    except Exception:
        return None


def get_user_name(user_id):
    try:
        ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
        ZENDESK_USER = os.environ.get("ZENDESK_USER")
        ZENDESK_URL = os.environ.get("ZENDESK_URL") + f"/api/v2/users/{user_id}"
        response = requests.get(ZENDESK_URL, auth=(ZENDESK_USER, ZENDESK_PASSWORD))
        resp = response.json()
        return resp["user"]["name"]
    except Exception:
        return None


def ticket_count():
    try:
        ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
        ZENDESK_URL = os.environ.get("ZENDESK_URL") + "/api/v2/tickets/count.json"
        ZENDESK_USER = os.environ.get("ZENDESK_USER")
        response = requests.get(
            ZENDESK_URL, auth=(ZENDESK_USER, ZENDESK_PASSWORD)
        ).json()
        return int(response["count"]["value"])
    except Exception:
        return None


def create_ticket_list_context(page=1):
    ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
    context = dict()
    context["error"] = False
    count = ticket_count()
    if count is None:
        context["error"] = True
        context[
            "error_message"
        ] = """
                😅 Ticket count is currently unavailanle.
                That means the API may not be available.
                Try again in a few minutes or contact asw15@sfu.ca for assistance.
            """
        return context
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
        for ticket in context["tickets"]:
            ticket["updated_at"] = datetime.datetime.strptime(
                ticket["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
            )
            ticket["created_at"] = datetime.datetime.strptime(
                ticket["created_at"], "%Y-%m-%dT%H:%M:%SZ"
            )
        context["has_less"] = current_page > 1
        context["prev_page"] = current_page - 1
        context["has_more"] = ceil(count / PER_PAGE) > page
        context["next_page"] = current_page + 1
        context["current_page"] = current_page
        context["max"] = ceil(count / PER_PAGE)
        context["count_in_page"] = len(context["tickets"])
        context["count_all"] = count
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


def create_ticket_detail_context(page=1, ticket_id=1):
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
        return context
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
        context["ticket"] = resp["ticket"]

        context["ticket"]["group_name"] = get_group_name(resp["ticket"]["group_id"])
        context["ticket"]["requester_name"] = get_user_name(
            resp["ticket"]["requester_id"]
        )

        context["ticket"]["updated_at"] = datetime.datetime.strptime(
            context["ticket"]["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
        )
        context["ticket"]["created_at"] = datetime.datetime.strptime(
            context["ticket"]["created_at"], "%Y-%m-%dT%H:%M:%SZ"
        )
        context["back_value"] = page
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
