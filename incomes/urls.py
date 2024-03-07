from django.urls import path 

from . import views

app_name = "incomes"

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:income_id>/edit', views.edit_income_item, name='edit_income_item'),
    path('<int:income_id>/save', views.save_income_item, name='save_income_item'),
    path('<int:income_id>/delete', views.delete_income_item, name='delete_income_item'),
    path('create', views.create_income_item, name='create_income_item'),
    path('search/', views.search, name='search'),
    path('automated_income', views.automated_income, name='automated_income'),
    path('create_automated_income', views.create_automated_income, name='create_automated_income')
]