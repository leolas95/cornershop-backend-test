import os
import urllib.parse
from http import HTTPStatus

import requests

from cornershop_backend_test.celery import app
from menus.models import MenuSelection
from slack.service_urls import LIST_USERS_URL, SEND_REMINDER_URL

SLACK_USER_TOKEN = os.getenv('SLACK_USER_TOKEN')


class SlackRetryException(Exception):
    def __init__(self, msg, retry_after):
        super().__init__(msg)
        self.msg = msg
        self.retry_after = retry_after

    def __reduce__(self):
        return SlackRetryException, (self.msg, self.retry_after)


def get_users_data():
    """Returns a list of the workspace members data, ignoring bots."""
    response = requests.get(
        LIST_USERS_URL,
        headers={'Authorization': f'Bearer {SLACK_USER_TOKEN}'},
    )

    if response.status_code == HTTPStatus.OK:
        users = response.json()['members']

        # Ignore bots
        return filter(lambda user: user['name'] != 'slackbot' and not user['is_bot'], users)

    return []


def build_selection_url(scheme: str, host: str, selection: MenuSelection):
    return urllib.parse.urlunsplit((scheme, host, selection.get_absolute_url(), '', ''))


@app.task(bind=True, rate_limit='3/s')
def _send_reminder(self, selection_url: str, user_id: str):
    """Make request to send reminders to members."""
    try:
        reminder_text = f"Hi! This is the link to select today's menu: {selection_url}"
        response = requests.post(
            SEND_REMINDER_URL,
            headers={'Authorization': f'Bearer {SLACK_USER_TOKEN}'},
            json={'text': reminder_text, 'time': 'in 2 seconds', 'user': user_id}
        )
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            retry_after = response.headers['Retry-After']
            raise SlackRetryException(f'Too many requests, retrying after {retry_after}', retry_after)
    except SlackRetryException as exc:
        # Retry request if Slack rate-limited us
        self.retry(exc=exc, countdown=int(exc.retry_after))


def send_reminders(menu_id: str, scheme: str, host: str):
    """Send slack reminders to appropriate members of the workspace."""

    users = get_users_data()
    for user in users:
        selection = MenuSelection.objects.create(
            menu_id=menu_id,
            slack_user_id=user['id'],
            slack_name=user['name'],
            slack_display_name=user['profile']['display_name']
        )
        selection_url = build_selection_url(scheme, host, selection)
        _send_reminder.delay(selection_url, user['id'])
