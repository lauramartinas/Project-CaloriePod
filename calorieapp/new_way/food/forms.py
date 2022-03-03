from django import forms

from calories.models import FoodPerDay, Food


class SelectFoodForm(forms.ModelForm):
    class Meta:
        model = FoodPerDay
        fields = ('food_selected', 'quantity',)

    def __init__(self, user, *args, **kwargs):
        super(SelectFoodForm, self).__init__(*args, **kwargs)
        self.fields['food_selected'].queryset = Food.objects.filter(person_of=user)


class AddFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('name', 'quantity', 'calorie')