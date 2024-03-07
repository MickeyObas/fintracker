from django.shortcuts import render
from django.http import JsonResponse

from .models import Category
from .serializers import CategorySerializer
from accounts.models import User

import json


def categories_list(request, user_id, category_type):
    user = User.objects.get(id=user_id)
    if request.user == user:
        user_categories = Category.objects.filter(user=user, type=category_type)
        serialized_data = CategorySerializer(user_categories, many=True).data
        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse(status=403)

def get_category(request):
    data = json.loads(request.body)
    category_id = data['categoryId']
    user_category = Category.objects.get(
        user=request.user,
        id=category_id
    )
    serialized_data = CategorySerializer(user_category).data

    return JsonResponse(serialized_data)

def save_category(request):
    data = json.loads(request.body)
    category_id = data['categoryId']
    updated_category_value = data['updatedCategoryValue']
    user_category_to_save = Category.objects.get(
        user=request.user,
        id=category_id
    )
    user_category_to_save.title = updated_category_value
    user_category_to_save.save()
    serialized_data = CategorySerializer(user_category_to_save).data

    return JsonResponse({
        'status': 'successful', 
        'category': serialized_data
    })

def create_category(request):
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title')
        is_automated = True if request.POST.get('automated') else False
        type = request.POST.get('type')

        new_category = Category.objects.create(
            user=request.user,
            title=title,
            is_automated=is_automated,
            type=type
        )

        user_categories = Category.objects.filter(
            user=request.user
        )

        serialized_data = CategorySerializer(user_categories, many=True).data

    return JsonResponse({
        'message': 'Category successfully created!',
        'user_categories': serialized_data
    })

def delete_category(request):
    data = json.loads(request.body)
    print(request.body)
    print(data)
    category_id = data['categoryId']
    category_to_delete = Category.objects.get(
        user=request.user,
        id=category_id
    )
    category_to_delete.delete()

    user_categories = Category.objects.filter(
            user=request.user
        )

    serialized_data = CategorySerializer(user_categories, many=True).data
    
    return JsonResponse({
        'message': 'Deletion successful!',
        'user_categories': serialized_data
    })

def categories(request):
    user_categories = Category.objects.filter(user=request.user)

    context = {
        "user_categories": user_categories
    }

    return render(request, 'settings/categories.html', context)

