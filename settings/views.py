from django.shortcuts import render
from django.http import JsonResponse

from accounts.models import User
from categories.models import Category
from categories.serializers import CategorySerializer

import json


def index(request):
    return render(request, "settings/index.html")

