from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

from food.models import Food, FoodCategory
from food.serializers import FoodListSerializer


# Create your views here.

class FoodCategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        published_food = Food.objects.filter(is_publish=True)

        categories_with_publ_foods = FoodCategory.objects.prefetch_related(
            Prefetch('food', queryset=published_food)
        ).filter(food__is_publish=True)

        if not categories_with_publ_foods.exists():
            return Response(
                {"detail": "No categories with published foods found."},
                status=HTTP_404_NOT_FOUND
            )

        serializer = FoodListSerializer(categories_with_publ_foods, many=True)

        return Response(serializer.data, status=HTTP_200_OK)
