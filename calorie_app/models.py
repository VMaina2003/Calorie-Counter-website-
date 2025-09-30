from django.db import models

# Create your models here.

# add any models you need for your calorie app here
# For example, you might want a model to represent food items and their calorie counts
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    amount = models.CharField(max_length=50, blank=True, null=True)
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('supper', 'Supper'),
        ('snack', 'Snack'),
    ]
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES, default='breakfast')
    date_added = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.name} - {self.calories} kcal"
    
    class Meta:
        ordering = ['-date_added']


class FoodCatalog(models.Model):
    """A simple catalog of common foods and their default calories (per serving).

    The user can search this table to auto-fill calorie values.
    """
    name = models.CharField(max_length=150, unique=True)
    calories = models.IntegerField(help_text='Calories per default serving')
    default_amount = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.calories} kcal"
    