from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from incomes.models import IncomeItem
from expenses.models import ExpenseItem
from incomes.serializers import IncomeItemSerializer
from expenses.serializers import ExpenseItemSerializer

from datetime import datetime, timedelta
from collections import Counter


@login_required(login_url='login')
def dashboard(request):
    user_expenses = ExpenseItem.objects.filter(user=request.user)[:6]
    user_incomes = IncomeItem.objects.filter(user=request.user)[:6]

    context = {
        'user_expense_items': user_expenses,
        'user_income_items': user_incomes
    }

    return render(request, "dashboard/dashboard.html", context)

def get_last_six_income_items(request):
    last_six_income_items = IncomeItem.objects.filter(user=request.user)[:6]
    serialized_data = IncomeItemSerializer(last_six_income_items, many=True).data

    return JsonResponse({
        'data': serialized_data
    })


def get_last_six_expense_items(request):
    last_six_expense_items = ExpenseItem.objects.filter(user=request.user)[:6]
    serialized_data = ExpenseItemSerializer(last_six_expense_items, many=True).data

    return JsonResponse({
        'data': serialized_data
    })

def get_last_six_transactions(request):

    end_date = datetime.now()
    start_date = end_date - timedelta(6)

    # Get the income items from the last six days
    incomes = IncomeItem.objects.filter(
        user=request.user,
        created__range=[start_date, end_date]
    ).values('created__date').annotate(total_income=Sum('amount'))

    # Get the expense items from the last six days
    expenses = ExpenseItem.objects.filter(
        user=request.user,
        created__range=[start_date, end_date]
    ).values('created__date').annotate(total_expense=Sum('amount'))

    # Store the last six dates into a list 
    date_range = [end_date - timedelta(i) for i in range(6)]
    labels = [date.strftime("%d-%m-%Y") for date in date_range]

    # Create a dictionary to store {date: expense_total} for last 6 days
    expense_totals = {expense['created__date'].strftime("%d-%m-%Y"): expense['total_expense'] for expense in expenses}
    expense_amounts = [expense_totals.get(date, 0) for date in labels]

    # Create a dictionary to store {date: income_total} for last 6 days
    income_totals = {income['created__date'].strftime("%d-%m-%Y"): income['total_income'] for income in incomes}
    income_amounts = [income_totals.get(date, 0) for date in labels]

    return JsonResponse({
        'labels': labels,
        'income_amounts': income_amounts,
        'expense_amounts': expense_amounts
    })
