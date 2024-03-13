from django.contrib import admin

from .models import IncomeItem, ScheduledIncomeItem


@admin.register(IncomeItem)
class ExpenseItemModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'amount', 'category', 'notes', 'created']


@admin.register(ScheduledIncomeItem)
class ScheduledExpenseItemModelAdmin(admin.ModelAdmin):
    list_display = ['source_income_item', 'frequency', 'last_process_time', 'is_active']
