from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from .models import ExpenseItem, ScheduledExpenseItem
from .serializers import ExpenseItemSerializer
from categories.models import Category

import json

def index(request):
    user_expense_items = ExpenseItem.objects.filter(user=request.user)[:5]
    
    # TODO: Find a way to use a custom template tag
    empty_rows = [x for x in range(5 - user_expense_items.count())]

    context = {
        "expense_items": user_expense_items,
        "empty_rows": empty_rows
    }

    return render(request, "expenses/index.html", context)

def create_expense_item(request):
    if request.method == 'POST':
        expense_title = request.POST.get('title')
        expense_amount = request.POST.get('amount')
        expense_category = request.POST.get('category')
        expense_notes = request.POST.get('notes')

        new_expense_item = ExpenseItem.objects.create(
            user=request.user,
            title=expense_title,
            amount=expense_amount,
            notes=expense_notes,
            category=Category.objects.get(
                user=request.user,
                title=expense_category,
                type='E')
        )

        user_expense_items = ExpenseItem.objects.filter(user=request.user)[:5]
        serialized_data = ExpenseItemSerializer(user_expense_items, many=True).data

        new_expense_item.save()
        return JsonResponse({
            'status': 'success',
            'expenses': serialized_data
        })

def edit_expense_item(request, expense_id):
    try:
        expense_to_edit = ExpenseItem.objects.get(id=expense_id, user=request.user)
        user_expense_categories = Category.objects.filter(user=request.user, type=Category.CategoryType.EXPENSE)
        print(user_expense_categories)
        return JsonResponse({
            "title": expense_to_edit.title,
            "amount": expense_to_edit.amount,
            "category": expense_to_edit.category.title,
            "notes": expense_to_edit.notes,
            'user-expense-categories': [category.title for category in user_expense_categories]
        })
    except ExpenseItem.DoesNotExist:
        return JsonResponse({
            "error": "Does not exist"
        })
    
def save_expense_item(request, expense_id):
    data = json.loads(request.body)
    print(data)
    try: 
        expense_to_save = ExpenseItem.objects.get(id=expense_id, user=request.user)
        expense_to_save.title = data['title']
        expense_to_save.category = Category.objects.get(user=request.user, title=data['category'], type='E')
        expense_to_save.notes = data['notes']
        expense_to_save.amount = data['amount']
        expense_to_save.save()
        return JsonResponse({
            'status': 'success',
        })
    except ExpenseItem.DoesNotExist:
        return JsonResponse({
            "error": "Does not exist!"
        })
    

def delete_expense_item(request, expense_id):
    try:
        print(request.body)
        expense_to_delete = ExpenseItem.objects.get(user=request.user, id=expense_id)
        expense_to_delete.delete()
        user_expense_items = ExpenseItem.objects.filter(user=request.user)[:5]
        serialized_data = ExpenseItemSerializer(user_expense_items, many=True).data

        return JsonResponse({
            'status': 'successful',
            'expenses': serialized_data,
        })
    
    except Exception as e:
        print("Whoops, ", e)
        print("The ID in question is" + str(expense_id))
        return JsonResponse({
            'status': 'An error occured'
        })
    
def search(request):
    q = request.GET.get('q')
    user_expenses = ExpenseItem.objects.filter(user=request.user)
    filtered_user_expenses = user_expenses.filter(
        Q(title__icontains=q) | Q(category__title__icontains=q) | Q(notes__icontains=q))[:5]
    
    serialized_data = ExpenseItemSerializer(filtered_user_expenses, many=True).data

    return JsonResponse({
        'expenses': serialized_data
    })

def automated_expense(request):
    frequency_choices = ScheduledExpenseItem.Frequency.choices
    user_categories = Category.objects.filter(
        user=request.user,
        type='E'
    )

    context = {
        "frequency_choices": frequency_choices,
        "user_categories": user_categories
    }

    return render(request, "expenses/automated_expense.html", context)

def create_automated_expense(request):
    expense_title = request.POST.get('title')
    expense_amount = request.POST.get('amount')
    expense_category = request.POST.get('category')
    expense_notes = request.POST.get('notes')
    frequency = request.POST.get('frequency')

    new_expense_item = ExpenseItem.objects.create(
        user=request.user,
        title=expense_title,
        amount=expense_amount,
        category=Category.objects.get(
            user=request.user,
            title=expense_category,
            type='E'
            ),
        notes=expense_notes
    )

    ScheduledExpenseItem.objects.create(
        source_expense_item=new_expense_item,
        frequency=frequency,
        is_active=True
    )

    serialized_data = ExpenseItemSerializer(new_expense_item).data

    return JsonResponse({
        'message': 'success',
        'expense': {
            'data': serialized_data,
            'frequency': frequency
        }
    })