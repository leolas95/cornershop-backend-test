from django.urls import path

from menus.views import CreateMenuView, DetailMenuView, ListMenuView, ListSelectionsView
from slack.views import SendReminderView, SelectMenuOptionView

app_name = 'menus'
urlpatterns = [
    path('', ListMenuView.as_view(), name='list_menus'),
    path('create/', CreateMenuView.as_view(), name='create_menu'),
    path('detail/<int:pk>/', DetailMenuView.as_view(), name='detail_menu'),
    path('send_reminder/<int:menu_id>', SendReminderView.as_view(), name='send_reminder'),
    path('<uuid:selection_uuid>/', SelectMenuOptionView.as_view(), name='select_menu_option'),
    path('selections/', ListSelectionsView.as_view(), name='list_selections'),
]