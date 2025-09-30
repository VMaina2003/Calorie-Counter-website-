from django.urls import path
from . import views

app_name = 'calorie_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_food, name='add_food'),
    path('foods/', views.view_foods, name='view_foods'),
    path('stats/', views.view_stats, name='view_stats'),
]
