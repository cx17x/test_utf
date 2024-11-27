# Food API Project

## Описание
Это проект REST API для управления блюдами и категориями блюд ресторана. API предоставляет возможность просматривать опубликованные блюда, сгруппированные по категориям.

## Техническое задание
1. **Модели**:
   - `FoodCategory`: Категории блюд.
   - `Food`: Блюда, связанные с категориями.
   
2. **Условия выборки данных**:
   - В выборку попадают только те блюда, у которых `is_publish=True`.
   - Если у категории нет блюд, или все блюда в категории имеют `is_publish=False`, такая категория не включается в ответ API.

3. **Эндпоинт**:
   - URL: `127.0.0.1/api/v1/foods/`
   - Метод: `GET`
   - Формат ответа: JSON
   
4. **Требования к запросу в базу данных**:
   - Запрос должен быть выполнен с использованием Django ORM (предпочтительно), Raw SQL или SQLAlchemy.

5. **Пример ответа API**:
   - Успешный запрос:
     ```json
     [
         {
             "id": 1,
             "name_ru": "Салаты",
             "foods": [
                 {
                     "internal_code": 101,
                     "name_ru": "Греческий салат",
                     "cost": "250.00"
                 }
             ]
         }
     ]
     ```
   - Если данных нет:
     ```json
     {
         "detail": "No categories with published foods found."
     }
     ```

## Реализация
### Основные компоненты:
1. **Модели**:
   - `FoodCategory` и `Food` (описаны в `food/models.py`).
2. **Сериализаторы**:
   - `FoodSerializer` и `FoodListSerializer` для преобразования данных моделей в формат JSON.
3. **Вьюха**:
   - `FoodCategoryListView` реализует логику выборки данных и обработки условий ТЗ.

### Используемый стек:
- **Django**: Фреймворк для построения веб-приложений.
- **Django REST Framework (DRF)**: Для реализации REST API.

### Запрос данных:
Выборка данных осуществляется через Django ORM с использованием фильтрации и prefetch:

```python
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FoodCategory, Food
from .serializers import FoodListSerializer

class FoodCategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        published_foods = Food.objects.filter(is_publish=True)
        categories_with_published_foods = FoodCategory.objects.prefetch_related(
            Prefetch('food', queryset=published_foods)
        ).filter(food__is_publish=True)
        
        if not categories_with_published_foods.exists():
            return Response({"detail": "No categories with published foods found."}, status=404)

        serializer = FoodListSerializer(categories_with_published_foods, many=True)
        return Response(serializer.data)
