from django.urls import path

from .views import  AddFood, FoodPerDay 
from .views import select_food,update_food,delete_food

app_name = 'food'

urlpatterns = [

    
    path('select_food/', select_food, name='select_food'),
	path('add_food/', AddFood.as_view(), name='add_food'),
	path('update_food/<str:pk>/', update_food, name='update_food'),
	path('delete_food/<str:pk>/', delete_food, name='delete_food'),
    path('profile/', FoodPerDay , name='profile'),
    

]