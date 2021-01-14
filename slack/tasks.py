import os
import urllib.parse
from http import HTTPStatus

import requests

from cornershop_backend_test.celery import app
from menus.models import MenuSelection
from slack.constants import LIST_USERS_URL, SEND_REMINDER_URL

SLACK_USER_TOKEN = os.getenv('SLACK_USER_TOKEN')


class SlackRetryException(Exception):
    def __init__(self, msg, retry_after):
        super().__init__(msg)
        self.msg = msg
        self.retry_after = retry_after

    def __reduce__(self):
        return SlackRetryException, (self.msg, self.retry_after)


def get_users():
    response = requests.get(
        LIST_USERS_URL,
        headers={'Authorization': f'Bearer {SLACK_USER_TOKEN}'},
    )
    members = response.json()['members']

    ids = []
    for member in members:
        if member['name'] == 'slackbot':
            continue
        if member['is_bot']:
            continue
        ids.append(member['id'])
    return ids


@app.task(bind=True, rate_limit='3/s')
def send_reminder(self, selection_url, user_id):
    try:
        response = requests.post(
            SEND_REMINDER_URL,
            headers={'Authorization': f'Bearer {SLACK_USER_TOKEN}'},
            json={'text': f'Hello world! {selection_url}', 'time': 'now', 'user': user_id}
        )
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            retry_after = response.headers['Retry-After']
            raise SlackRetryException(f'Too many requests, retrying after {retry_after}', retry_after)
    except SlackRetryException as exc:
        self.retry(exc=exc, countdown=int(exc.retry_after))


def send_reminders(menu_id, scheme, host):
    users = get_users()
    for user_id in users:
        selection = MenuSelection.objects.create(menu_id=menu_id, slack_user_id=user_id)
        selection_url = urllib.parse.urlunsplit((scheme, host, selection.get_absolute_url(), '', ''))
        send_reminder.delay(selection_url, user_id)
