Cornershop's backend test
=========================

The project consists of three main apps:
1. The `users` app contains the model for users, as well as the views and templates for user signup, login, logout,
   and profile.
2. The `menus` app contains the models, views and templates used for menu creation.
3. The `slack` app contains the integration with the Slack API, allowing to send the menu of the day to the associated
workspace's members. Currently, there's no way of associating slack users with system users beyond the registered names.