from django.urls import path

from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create_expense_item, name='create_expense_item'),
    path('<int:expense_id>/edit', views.edit_expense_item, name='edit_expense_item'),
    path('<int:expense_id>/delete', views.delete_expense_item, name='delete_expense_item'),
    path('<int:expense_id>/save', views.save_expense_item, name='save_expense_item'),
    path('search/', views.search, name='search'),
    path('automated_expense', views.automated_expense, name='automated_expense'),
    path('create_automated_expense', views.create_automated_expense, name='create_automated_expense')
]