from django.db import models

from core.models import TimeStampedModel
from accounts.models import User
from categories.models import Category


class ExpenseItem(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey("categories.Category", on_delete=models.SET_DEFAULT, default=None)
    notes = models.CharField(max_length=255, blank=True, null=True)
    is_automated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.user.first_name}: {self.title} Cost: {self.amount}"
    

class ScheduledExpenseItem(models.Model):

    class Frequency(models.TextChoices):
        SECONDLY = 'secondly', "Secondly"
        DAILY = 'daily', "Daily"
        WEEKLY = 'weekly', "Weekly"
        MONTHLY = 'monthly', "Monthly"
        YEARLY = 'yearly', "Yearly"

    source_expense_item = models.ForeignKey(ExpenseItem, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=20, null=True, choices=Frequency.choices)
    created = models.DateTimeField(auto_now_add=True)
    last_process_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Automating: {self.source_expense_item}"