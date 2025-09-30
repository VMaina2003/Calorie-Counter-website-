from django.shortcuts import render, redirect
from .models import FoodItem
from django.db.models import Sum
from .models import FoodCatalog
from django.utils import timezone




# Create your views here.
def index(request):
    # Show today's summary: total calories and recent entries
    today = timezone.localdate()
    start = timezone.datetime.combine(today, timezone.datetime.min.time(), tzinfo=timezone.get_current_timezone())
    end = timezone.datetime.combine(today, timezone.datetime.max.time(), tzinfo=timezone.get_current_timezone())

    todays_foods = FoodItem.objects.filter(date_added__range=(start, end)).order_by('-date_added')
    total_calories = todays_foods.aggregate(Sum('calories'))['calories__sum'] or 0

    return render(request, 'calorie/index.html', {
        'todays_foods': todays_foods,
        'today_total': total_calories,
    })


def add_food(request):
    context = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name')
        calories = request.POST.get('calories')
        amount = request.POST.get('amount', '')
        meal_type = request.POST.get('meal_type', 'breakfast')

        # 'check' action: look up the catalog and show suggestion
        if action == 'check' and name:
            try:
                catalog_item = FoodCatalog.objects.get(name__iexact=name.strip())
                context['suggested_calories'] = catalog_item.calories
                context['suggested_amount'] = catalog_item.default_amount
                context['name'] = catalog_item.name
                context['meal_type'] = meal_type
            except FoodCatalog.DoesNotExist:
                context['error'] = 'Food not found in catalog.'

            return render(request, 'calorie/add_food.html', context)

        # 'save' action: validate and persist to FoodItem
        if action == 'save' and name and calories:
            try:
                calories_int = int(calories)
            except ValueError:
                context['error'] = 'Calories must be a number.'
                return render(request, 'calorie/add_food.html', context)

            food_item = FoodItem(name=name.strip(), calories=calories_int, amount=amount, meal_type=meal_type)
            food_item.save()
            return redirect('calorie_app:view_foods')

        context['error'] = 'Please provide the food name and calories before saving.'

    return render(request, 'calorie/add_food.html', context)


def view_foods(request):
    foods = FoodItem.objects.all().order_by('-date_added')
    return render(request, 'calorie/view_foods.html', {'foods': foods})


def view_stats(request):
    total_calories = FoodItem.objects.aggregate(Sum('calories'))['calories__sum'] or 0
    food_count = FoodItem.objects.count()
    average_calories = total_calories / food_count if food_count > 0 else 0
    return render(request, 'calorie/stats.html', {
        'total_calories': total_calories,
        'food_count': food_count,
        'average_calories': round(average_calories, 2)
    })


