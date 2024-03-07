from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from .models import IncomeItem, ScheduledIncomeItem
from .serializers import IncomeItemSerializer
from categories.models import Category

import json

def index(request):
    user_incomes = IncomeItem.objects.filter(user=request.user)[:5]

     # TODO: Find a way to use a custom template tag
    empty_rows = [x for x in range(5 - user_incomes.count())]

    context = {
        'user_incomes': user_incomes,
        'empty_rows': empty_rows
    }

    return render(request, "incomes/index.html", context)

def edit_income_item(request, income_id):
    try:
        income_to_edit = IncomeItem.objects.get(user=request.user, id=income_id)
        user_income_categories = Category.objects.filter(
            user=request.user,
            type=Category.CategoryType.INCOME
        )
        return JsonResponse({
            "title": income_to_edit.title,
            "amount": income_to_edit.amount,
            "category": income_to_edit.category.title,
            "notes": income_to_edit.notes,
            'user-income-categories': [category.title for category in user_income_categories]
        })
    except IncomeItem.DoesNotExist:
        return JsonResponse({
            "error": "Does not exist"
        })
    
def save_income_item(request, income_id):
    data = json.loads(request.body)
    print(data)
    try:
        income_to_save = IncomeItem.objects.get(user=request.user, id=income_id)
        income_to_save.title = data['title']
        income_to_save.amount = data['amount']
        income_to_save.notes = data['notes']
        income_to_save.category = Category.objects.get(
            user=request.user,
            title=data['category'],
            type='I'
        )
        income_to_save.save()
        return JsonResponse({
            'status': 'success',
        })
    except IncomeItem.DoesNotExist:
        return JsonResponse({
            "error": "Does not exist"
        })

def delete_income_item(request, income_id):
    try:
        print(request.body)
        income_to_delete = IncomeItem.objects.get(user=request.user, id=income_id)
        income_to_delete.delete()
        user_income_items = IncomeItem.objects.filter(user=request.user)[:5]
        serialized_data = IncomeItemSerializer(user_income_items, many=True).data

        return JsonResponse({
            'status': 'successful',
            'incomes': serialized_data,
        })
    
    except Exception as e:
        print("Whoops, ", e)
        print("The ID in question is" + str(income_id))
        return JsonResponse({
            'status': 'An error occured'
        })
    
def create_income_item(request):
    if request.method == 'POST':
        income_title = request.POST.get('title')
        income_amount = request.POST.get('amount')
        income_category = request.POST.get('category')
        income_notes = request.POST.get('notes')

        new_income_item = IncomeItem.objects.create(
            user=request.user,
            title=income_title,
            amount=income_amount,
            notes=income_notes,
            category=Category.objects.get(
                user=request.user,
                title=income_category,
                type='I'
                )
        )

        user_income_items = IncomeItem.objects.filter(user=request.user)[:5]
        serialized_data = IncomeItemSerializer(user_income_items, many=True).data

        new_income_item.save()
        return JsonResponse({
            'status': 'success',
            'incomes': serialized_data
        })

def search(request):
    q = request.GET.get('q')
    user_expenses = IncomeItem.objects.filter(user=request.user)
    filtered_user_incomes = user_expenses.filter(
        Q(title__icontains=q) | Q(category__title__icontains=q) | Q(notes__icontains=q))[:5]
    
    serialized_data = IncomeItemSerializer(filtered_user_incomes, many=True).data

    return JsonResponse({
        'incomes': serialized_data
    })

def automated_income(request):
    frequency_choices = ScheduledIncomeItem.Frequency.choices
    user_categories = Category.objects.filter(
        user=request.user,
        type='I'
    )

    context = {
        "frequency_choices": frequency_choices,
        "user_categories": user_categories
    }

    return render(request, "incomes/automated_income.html", context)

def create_automated_income(request):
    income_title = request.POST.get('title')
    income_amount = request.POST.get('amount')
    income_category = request.POST.get('category')
    income_notes = request.POST.get('notes')
    frequency = request.POST.get('frequency')

    new_income_item = IncomeItem.objects.create(
        user=request.user,
        title=income_title,
        amount=income_amount,
        category=Category.objects.get(
            user=request.user,
            title=income_category,
            type='I'
            ),
        notes=income_notes
    )

    ScheduledIncomeItem.objects.create(
        source_income_item=new_income_item,
        frequency=frequency,
        is_active=True
    )

    serialized_data = IncomeItemSerializer(new_income_item).data

    return JsonResponse({
        'message': 'success',
        'income': {
            'data': serialized_data,
            'frequency': frequency
        }
    })