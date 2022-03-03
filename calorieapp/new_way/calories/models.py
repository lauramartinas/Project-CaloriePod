
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from datetime import date
from food.models import Food


# Create your models here.

class CalorieGoal(models.Model):
    person_of = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    calorie_goal = models.PositiveIntegerField(default=0)



class FoodPerDay(models.Model):

    person_of = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    calorie_count = models.FloatField(default=0, null=True, blank=True)
    food_selected = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.FloatField(default=0)
    total_calorie = models.FloatField(default=0, null=True)
    date = models.DateField(auto_now_add=True)   
    food_today = models.ManyToManyField(Food, through='PostFood', related_name='inventory')


    def save(self, *args, **kwargs):  # new
           
        if self.food_selected != None:
            self.total_calorie = self.quantity * self.food_selected.calorie
            
            super(FoodPerDay, self).save(*args, **kwargs)
            

      
    def __str__(self):
        return str(self.person_of.username)

    def __str__(self):
        return self.food_selected

class PostFood(models.Model):

    profile = models.ForeignKey(FoodPerDay, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    calorie_amount = models.FloatField(default=0, null=True, blank=True)
    amount = models.FloatField(default=0)
