from django.utils import timezone

from .models import IncomeItem, ScheduledIncomeItem
from accounts.models import User
from categories.models import Category

from celery import shared_task
from datetime import datetime, timedelta


@shared_task()
def add(x, y):
    return x + y

@shared_task()
def handle_scheduled_transactions(*args, **kwargs):
    # Find way to get only due-to-reschedule transactions
    scheduled_income_items = ScheduledIncomeItem.objects.all()

    for scheduled_income_item in scheduled_income_items:
        if scheduled_income_item.is_active:
            timegap = timezone.now() - scheduled_income_item.last_process_time
            source_income_item = scheduled_income_item.source_income_item
            
            if scheduled_income_item.frequency == 'daily':
                difference_in_hours = timegap.total_seconds() // 3600
                if difference_in_hours >= 24:
                    IncomeItem.objects.create(
                        user=source_income_item.user,
                        title=source_income_item.title,
                        amount=source_income_item.amount,
                        category=source_income_item.category,
                        notes=source_income_item.notes
                    )
                    scheduled_income_item.last_process_time = datetime.now()
                    scheduled_income_item.save()
            elif scheduled_income_item.frequency == 'secondly':
                # TEST MODE
                difference_in_seconds = timegap.total_seconds()
                if difference_in_seconds >= 30:
                    IncomeItem.objects.create(
                        user=source_income_item.user,
                        title=source_income_item.title,
                        amount=source_income_item.amount,
                        category=source_income_item.category,
                        notes=source_income_item.notes
                    )
                    scheduled_income_item.last_process_time = datetime.now()
                    scheduled_income_item.save()
            elif scheduled_income_item.frequency == 'weekly':
                difference_in_days = timegap.days
                if difference_in_days >= 7:
                    IncomeItem.objects.create(
                        user=source_income_item.user,
                        title=source_income_item.title,
                        amount=source_income_item.amount,
                        category=source_income_item.category,
                        notes=source_income_item.notes
                    )
                    scheduled_income_item.last_process_time = datetime.now()
                    scheduled_income_item.save()
            elif scheduled_income_item.frequency == 'monthly':
                difference_in_days = timegap.days
                if difference_in_days >= 30:
                    IncomeItem.objects.create(
                        user=source_income_item.user,
                        title=source_income_item.title,
                        amount=source_income_item.amount,
                        category=source_income_item.category,
                        notes=source_income_item.notes
                    )
                    scheduled_income_item.last_process_time = datetime.now()
                    scheduled_income_item.save()
            elif scheduled_income_item.frequency == 'yearly':
                difference_in_days = timegap.days
                if difference_in_days >= 365:
                    IncomeItem.objects.create(
                        user=source_income_item.user,
                        title=source_income_item.title,
                        amount=source_income_item.amount,
                        category=source_income_item.category,
                        notes=source_income_item.notes
                    )
                    scheduled_income_item.last_process_time = datetime.now()
                    scheduled_income_item.save()

    print("All Clear!")