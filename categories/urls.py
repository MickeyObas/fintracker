from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('<int:user_id>/<str:category_type>', views.categories_list, name="categories_list"),
    path('category', views.get_category, name='get_category'),
    path('categories', views.categories, name='categories'),
    path('save_category', views.save_category, name='save_category'),
    path('create_category', views.create_category, name='create_category'),
    path('delete', views.delete_category, name='delete_category')
]