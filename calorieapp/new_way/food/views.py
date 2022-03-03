from audioop import add, reverse
import imp
from unicodedata import name
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from food.filters import FoodFilter
from calories.models import CalorieGoal, FoodPerDay, Food
from .forms import SelectFoodForm, AddFoodForm
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
# Create your views here.


class AddFood(ListView):
    model = Food
    template_name = 'add_food.html'
    paginate_by = 5

    def post(self,request):
        form = AddFoodForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.person_of = request.user
            profile.save()
            return redirect('food:add_food')

    def get_queryset(self):  
        return Food.objects.filter(person_of=self.request.user)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddFoodForm()
        return context


# for updating food given by the user
@login_required

def update_food(request, pk):
    food_items = Food.objects.filter(person_of=request.user)

    food_item = Food.objects.get(id=pk)
    form = AddFoodForm(instance=food_item)
    if request.method == 'POST':
        form = AddFoodForm(request.POST, instance=food_item)
        if form.is_valid():
            form.save()
            return redirect('calories:calprofile')
    myfilter = FoodFilter(request.GET, queryset=food_items)
    context = {'form': form, 'food_items': food_items, 'myfilter': myfilter}

    return render(request, 'add_food.html', context)


# for deleting food given by the user
@login_required

def delete_food(request, pk):
    food_item = Food.objects.get(id=pk)
    if request.method == "POST":
        food_item.delete()
        return redirect('calories:calprofile')
    context = {'food': food_item, }

    return render(request, 'delete_food.html', context) 


@login_required
def select_food(request):

    # for showing all food items available
    food_items = Food.objects.filter(person_of=request.user)
    form = SelectFoodForm(request.user)

    if request.method == 'POST':
        form = SelectFoodForm(request.user, request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.person_of = request.user
            instance.calorie_count = CalorieGoal.objects.get(person_of=request.user).calorie_goal
            instance.save()
            return redirect('/')
    else:
        form = SelectFoodForm(request.user)

    context = {'form': form, 'food_items': food_items}
    return render(request, 'select_food.html', context)

