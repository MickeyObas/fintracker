
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Category
from accounts.models import User
from expenses.models import ExpenseItem
from incomes.models import IncomeItem


@receiver(post_save, sender=User)
def create_default_category(sender, instance, created, **kwargs):
    if created:
        # Create default 'uncategorized' categories
        uncategorized_expense_category, _ = Category.objects.get_or_create(
            user=instance,
            title='Uncategorized',
            type='E'
        )
        uncategorized_income_category, _ = Category.objects.get_or_create(
            user=instance,
            title='Uncategorized',
            type='I'
        )

        # Create common Expense categories
        Category.objects.create(
            user=instance,
            title='Groceries',
            type='E'
        )
        Category.objects.create(
            user=instance,
            title='Bills',
            type='E'
        )
        Category.objects.create(
            user=instance,
            title='Subscription',
            type='E'
        )

        # Create common Income categories
        Category.objects.create(
            user=instance,
            title='Salary',
            type='I'
        )
        Category.objects.create(
            user=instance,
            title='Wages',
            type='I'
        )

@receiver(pre_delete, sender=Category)
def handle_category_deletion(sender, instance, **kwargs):
    user = instance.user
    category_type = instance.type

    uncategorized_expense_category, _ = Category.objects.get_or_create(
            user=user,
            title='Uncategorized',
            type='E'
        )
    uncategorized_income_category, _ = Category.objects.get_or_create(
        user=user,
        title='Uncategorized',
        type='E'
    )

    if category_type == 'E':
        ExpenseItem.objects.filter(user=user, category=instance).update(
            category=uncategorized_expense_category
        )
    if category_type == 'I':
        IncomeItem.objects.filter(user=user, category=instance).update(
            category=uncategorized_income_category
        )
        