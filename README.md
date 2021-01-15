Cornershop's backend test
=========================

The project consists of three main apps:
1. The `users` app contains the model for users, as well as the views and templates for user signup, login, logout,
   and profile.
2. The `menus` app contains the models, views and templates used for menu creation.
3. The `slack` app contains the integration with the Slack API, allowing to send the menu of the day to the associated
workspace members. Currently, there's no way of associating slack users with system users beyond seeing the registered names when users select a menu option.

First, users can be created either as Manager (who can create menus, send reminders, see other employees selections) or Employee (normal users that can only see and select a menu option, receive Slack reminders). This separation is pure logical, as both use the same model (Employee model), the only difference is the `is_staff` field, being True for managers and False for normal employees.
