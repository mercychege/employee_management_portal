from django.db import models
import datetime

class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


    def all_employees(self):
        return super().get_queryset()

    def all_active_employees(self):
        return super().get_queryset().filter(is_blocked=False)

    def all_blocked_employees(self):
        return super().get_queryset().filter(is_blocked=True)

    def birthdays_current_month(self):
        current_date = datetime.date.today()
        return super().get_queryset().filter(is_blocked = False).filter(dateofbirth__month = current_date.month)


