
import os
from random import randint
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'calorie_app.settings'
# $env:DJANGO_SETTINGS_MODULE = 'calorie_app.settings'
django.setup()
from django.db.models import F
from users.models import AuthUser
from calories.models import Food
# from posts.models import Post

# nUser  = AuthUser(email="test@test.com")

# nUser.save()
max_users = AuthUser.objects.count()
print(randint(1,max_users))


person = AuthUser.objects.get(id=1)
food = Food(name="test",quantity="1",calorie="1",person_of=person)
food.save()





