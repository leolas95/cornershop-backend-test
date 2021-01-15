import datetime
from unittest.mock import patch

from django.test import TestCase

from menus.models import Menu, MenuSelection
from slack.tasks import send_reminders, get_users_data


class SendRemindersTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.mock_users_data = [
            {
                'id': 'testid',
                'name': 'test',
                'profile': {
                    'display_name': 'Test'
                }
            },
            {
                'id': 'testid2',
                'name': 'test2',
                'profile': {
                    'display_name': 'Test2'
                }
            }
        ]

    @patch('slack.tasks.get_users_data')
    @patch('slack.tasks.send_reminder.delay')
    def test_should_call_task_when_sending_reminders(self, task_mock, data_mock):
        old_count = MenuSelection.objects.count()

        data_mock.return_value = self.mock_users_data
        menu = Menu.objects.create(date=datetime.date.today())

        send_reminders(menu.id, 'http', 'localhost:8000')

        task_mock.assert_called()

        new_count = MenuSelection.objects.count()

        self.assertEqual(new_count, old_count + 2)

    @patch('slack.tasks.requests.get')
    def test_get_users_data_should_return_empty_list_on_error(self, mock_get):
        mock_get.return_value.ok = False

        data = get_users_data()
        self.assertEqual(data, [])
