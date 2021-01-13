import requests
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View

from menus.forms import MenuForm
from menus.models import Menu, MenuSelection
from django.utils import timezone


LIMIT_HOUR = timezone.now().time().replace(hour=11, minute=0, second=0, microsecond=0)


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


def send_reminder(users, menu_id, request):
    for user_id in users:
        selection = MenuSelection.objects.create(menu_id=menu_id, slack_user_id=user_id)
        selection_url = request.build_absolute_uri(reverse('select_menu_option', kwargs={'selection_uuid': selection.id}))
        response = requests.post(
            'https://slack.com/api/reminders.add',
            headers={'Authorization': 'Bearer xoxp-1622044669637-1637762199217-1649177671232-3fa7fe1f4792d04468b6472ee4f76599'},
            json={'text': f'Hello world! {selection_url}', 'time': 'in 5 seconds', 'user': user_id}
        )


class SendReminderView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, menu_id):
        users = get_users()
        send_reminder(users, menu_id, request)
        return redirect('list_menus')


class SelectMenuOptionView(View):
    def get(self, request, selection_uuid):
        selection = get_object_or_404(MenuSelection, id=selection_uuid)
        form = MenuForm(instance=selection.menu)
        return render(request, 'select_option.html', {'form': form})

    def post(self, request, selection_uuid):
        if timezone.now().time() > LIMIT_HOUR:
            return HttpResponse(
                f'Time\'s up! Limit time to pick an option is {LIMIT_HOUR} CLT! Better luck next day'
            )

        selection = get_object_or_404(MenuSelection, id=selection_uuid)
        form = MenuForm(request.POST, instance=selection.menu)

        if form.is_valid():
            selection.option = form.cleaned_data['options']
            selection.save()
            return HttpResponse('Ok, thanks! Have a good meal :)')

        return HttpResponse('Error: option selection not valid')
