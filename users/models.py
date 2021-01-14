from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    """General model to for users of the management system.
    Virtually there's to kind of users: Manager, and Employee.

    Employees, besides signing up and login in, can only select
    a menu option for the link that was provided to them in the Slack reminder.

    A Manager can create and see the menus, as well as sending the reminders

    The differences between each is made by the is_staff field: Manager has this
    field as True, whereas a Employee has it as False
    """
    def __str__(self):
        return self.username
