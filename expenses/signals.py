from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ExpenseItem, ScheduledExpenseItem
from accounts.models import User
from categories.models import Category

from datetime import datetime, timedelta


@receiver(post_save, sender=ExpenseItem)
def create_scheduled_expense_item(sender, instance, created, **kwargs):
    if created and instance.is_automated:
        ScheduledExpenseItem.objects.create(
            source_expense_item=instance,
        )
