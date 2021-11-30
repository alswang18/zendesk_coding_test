import os
import traceback

import requests


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


def create_ticket_list_context(page=""):
    ZENDESK_PASSWORD = os.environ.get("ZENDESK_PASSWORD")
    if page == "":
        ZENDESK_URL = os.environ.get("ZENDESK_URL") + "/api/v2/tickets/?page[size]=25"
    else:
        ZENDESK_URL = page
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
        context["has_more"] = bool(resp["meta"]["has_more"])
        context["links_next"] = resp["links"]["next"]
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
