from django.urls import path 

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("incomes", views.get_last_six_income_items, name='incomes'),
    path("expenses", views.get_last_six_expense_items, name='expenses'),
    path('transactions', views.get_last_six_transactions, name='get_last_six_transactions')
]