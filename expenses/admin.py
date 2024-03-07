from django.contrib import admin

from .models import ExpenseItem, ScheduledExpenseItem
@admin.register(ExpenseItem)
class ExpenseItemModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'amount', 'category', 'notes', 'created']


@admin.register(ScheduledExpenseItem)
class ScheduledExpenseItemModelAdmin(admin.ModelAdmin):
    list_display = ['source_expense_item', 'frequency', 'last_process_time', 'is_active']