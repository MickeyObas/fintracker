from django.utils import timezone

from .models import ExpenseItem
from accounts.models import User
from categories.models import Category
from expenses.models import ExpenseItem, ScheduledExpenseItem
from incomes.models import IncomeItem, ScheduledIncomeItem

from celery import shared_task
from datetime import datetime, timedelta


@shared_task()
def handle_scheduled_transactions(*args, **kwargs):
    # Find way to get only due-to-reschedule transactions
    scheduled_expense_items = ScheduledExpenseItem.objects.all()

    for scheduled_expense_item in scheduled_expense_items:
        if scheduled_expense_item.is_active:
            timegap = timezone.now() - scheduled_expense_item.last_process_time
            source_expense_item = scheduled_expense_item.source_expense_item
            
            if scheduled_expense_item.frequency == 'daily':
                difference_in_hours = timegap.total_seconds() // 3600
                if difference_in_hours >= 24:
                    ExpenseItem.objects.create(
                        user=source_expense_item.user,
                        title=source_expense_item.title,
                        amount=source_expense_item.amount,
                        category=source_expense_item.category,
                        notes=source_expense_item.notes
                    )
                    scheduled_expense_item.last_process_time = datetime.now()
                    scheduled_expense_item.save()
            elif scheduled_expense_item.frequency == 'secondly':
                # TEST MODE
                difference_in_seconds = timegap.total_seconds()
                if difference_in_seconds >= 30:
                    ExpenseItem.objects.create(
                        user=source_expense_item.user,
                        title=source_expense_item.title,
                        amount=source_expense_item.amount,
                        category=source_expense_item.category,
                        notes=source_expense_item.notes
                    )
                    scheduled_expense_item.last_process_time = datetime.now()
                    scheduled_expense_item.save()
            elif scheduled_expense_item.frequency == 'weekly':
                difference_in_days = timegap.days
                if difference_in_days >= 7:
                    ExpenseItem.objects.create(
                        user=source_expense_item.user,
                        title=source_expense_item.title,
                        amount=source_expense_item.amount,
                        category=source_expense_item.category,
                        notes=source_expense_item.notes
                    )
                    scheduled_expense_item.last_process_time = datetime.now()
                    scheduled_expense_item.save()
            elif scheduled_expense_item.frequency == 'monthly':
                difference_in_days = timegap.days
                if difference_in_days >= 30:
                    ExpenseItem.objects.create(
                        user=source_expense_item.user,
                        title=source_expense_item.title,
                        amount=source_expense_item.amount,
                        category=source_expense_item.category,
                        notes=source_expense_item.notes
                    )
                    scheduled_expense_item.last_process_time = datetime.now()
                    scheduled_expense_item.save()
            elif scheduled_expense_item.frequency == 'yearly':
                difference_in_days = timegap.days
                if difference_in_days >= 365:
                    ExpenseItem.objects.create(
                        user=source_expense_item.user,
                        title=source_expense_item.title,
                        amount=source_expense_item.amount,
                        category=source_expense_item.category,
                        notes=source_expense_item.notes
                    )
                    scheduled_expense_item.last_process_time = datetime.now()
                    scheduled_expense_item.save()

    print("All Clear!")