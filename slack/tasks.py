import urllib.parse

import requests

from cornershop_backend_test.celery import app
from menus.models import MenuSelection


def get_users():
    response = requests.get(
        'https://slack.com/api/users.list',
        headers={'Authorization': 'Bearer xoxb-1622044669637-1649020734528-peRCE5T2yrWla5O9K6xkbz7r'},
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


@app.task
def send_reminder(menu_id, scheme, host):
    users = get_users()
    for user_id in users:
        selection = MenuSelection.objects.create(menu_id=menu_id, slack_user_id=user_id)
        selection_url = urllib.parse.urlunsplit((scheme, host, selection.get_absolute_url(), '', ''))
        requests.post(
            'https://slack.com/api/reminders.add',
            headers={'Authorization': 'Bearer xoxp-1622044669637-1637762199217-1649177671232-3fa7fe1f4792d04468b6472ee4f76599'},
            json={'text': f'Hello world! {selection_url}', 'time': 'now', 'user': user_id}
        )