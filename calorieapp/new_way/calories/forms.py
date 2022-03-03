from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.contrib.auth.models import User
from .models import CalorieGoal, Food, FoodPerDay


class CalProfileForm(forms.ModelForm):
    class Meta:
        model = FoodPerDay
        fields = ('food_selected', 'quantity',)

    def __init__(self, user, *args, **kwargs):
        super(CalProfileForm, self).__init__(*args, **kwargs)
        self.fields['food_selected'].queryset = Food.objects.filter(person_of=user)



class ProfileForm(forms.ModelForm):
    class Meta:
        model = CalorieGoal
        fields = ('calorie_goal',)

    def __init__(self, user, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        try:
           self.initial['calorie_goal'] = CalorieGoal.objects.get(person_of=user).calorie_goal
        except ObjectDoesNotExist:
            self.initial['calorie_goal'] = 0