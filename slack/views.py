import requests
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views import View


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


def send_reminder(users):
    for user_id in users:
        response = requests.post(
            'https://slack.com/api/reminders.add',
            headers={'Authorization': 'Bearer xoxp-1622044669637-1637762199217-1649177671232-3fa7fe1f4792d04468b6472ee4f76599'},
            json={'text': 'Hello world!', 'time': 'in 5 seconds', 'user': user_id}
        )


class SendReminderView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, menu_id):
        users = get_users()
        send_reminder(users)
        return redirect('list_menus')


