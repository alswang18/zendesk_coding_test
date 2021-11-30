#!/bin/bash
read -r -p "Do you want to enter your details in the cli rather than using an env? [y/N] " response
case "$response" in
    [yY][eE][sS]|[yY])
        read -r -p "Enter variable for ZENDESK_URL: " zendesk_url
        read -r -p "Enter variable for ZENDESK_USER: " zendesk_user
        echo "Enter variable for ZENDESK_PASSWORD: "
        read -r -s zendesk_password
        export ZENDESK_URL=$zendesk_url
        export ZENDESK_USER=$zendesk_user
        export ZENDESK_PASSWORD=$zendesk_password
        export USE_DOT_ENV=0 #0 is false 1 is true
        ;;
    *)
        echo "Using /ticket_viewer/.env if it exists."
        export USE_DOT_ENV=1
        ;;
esac