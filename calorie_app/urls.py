from django.urls import include, path

from . import routes

urlpatterns = [
    path('', include((routes.urlpatterns, 'calorie_app'), namespace='calorie_app')),
]