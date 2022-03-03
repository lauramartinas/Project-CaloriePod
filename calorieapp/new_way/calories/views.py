from django.views.generic import ListView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from calories.forms import ProfileForm
from calories.models import FoodPerDay
from django.db.models import Sum

#  ContactForm
from .models import *
from datetime import timedelta
from django.utils import timezone
from datetime import date
from datetime import datetime


def calprofile(request):
    if request.method == 'GET':
        form = ProfileForm(request.user.id)

    elif request.method == "POST":
        form = ProfileForm(request.user.id, request.POST)

        if form.is_valid():
            CalorieGoal.objects.update_or_create(person_of_id=request.user.id,defaults={
                'calorie_goal': form.cleaned_data['calorie_goal']
            })


    return render(request, "calprofile.html", {'form':ProfileForm(request.user.id), 'food_items':Food.objects.filter(person_of_id=request.user.id)})

class CalProfile(ListView):
    model = FoodPerDay
    template_name = 'calprofile.html'


    def post(self,request):
        form = ProfileForm(request.user.id,request.POST)
        if form.is_valid():
            CalorieGoal.objects.update_or_create(person_of_id=request.user.id,defaults={
                'calorie_goal': form.cleaned_data['calorie_goal']
            })
        return redirect('calories:calprofile')

    def get_queryset(self):  
        return FoodPerDay.objects.filter(person_of=self.request.user).values('date').annotate(
            total=Sum('total_calorie')).values_list(
                'date','total','calorie_count')
      
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfileForm(self.request.user.id)
        context['food_items'] = Food.objects.filter(person_of_id=self.request.user.id)
        return context



@login_required(login_url='users:login')

def HomePageView(request):
    return render(request, 'home.html')

@login_required(login_url='users:login')

def CalProfilePageView(request):
    # taking the latest profile object
    context = {
        'total_calorie': '',
        'calorie_goal': '',
        'calorie_goal_status': '',
        'over_calorie': '',
        'food_selected_today': '',
    }
    # default values
    try:    
        calories_goal = CalorieGoal.objects.get(person_of=request.user).calorie_goal
    except CalorieGoal.DoesNotExist:
        calories_goal = 0

    foods_today = FoodPerDay.objects.filter(person_of=request.user,date=datetime.now().date())
    food_today = 0
    for f in foods_today:
        food_today += f.total_calorie



    calorie_goal_status = calories_goal - food_today
    
    over_calorie = 0
    if calorie_goal_status < 0:
        over_calorie = abs(calorie_goal_status)
    
    context = {
    'total_calorie': int(food_today),
    'calorie_goal': calories_goal,
    'calorie_goal_status': calorie_goal_status,
    'over_calorie': over_calorie,
    'food_selected_today': foods_today,

    }
   

    return render(request, 'home.html', context)