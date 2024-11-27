from django.urls import path

from food.views import FoodCategoryListView

urlpatterns = [
    path('foods/', FoodCategoryListView.as_view(), name='food-category-list'),
]
