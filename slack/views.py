from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views import View

from menus.forms import MenuForm
from menus.models import MenuSelection
from slack.tasks import send_reminders

LIMIT_HOUR = timezone.now().time().replace(hour=11, minute=0, second=0, microsecond=0)


class SendReminderView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, menu_id):
        scheme = request.scheme
        host = request.get_host()
        send_reminders(menu_id, scheme, host)
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

        form = MenuForm(instance=selection.menu)
        return render(request, 'select_option.html', {'form': form})
