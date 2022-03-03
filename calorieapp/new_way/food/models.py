from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


# Create your models here.

class Food(models.Model):

    name = models.CharField(max_length=200, null=False)
    quantity = models.PositiveIntegerField(null=False, default=0)
    calorie = models.FloatField(null=False, default=0)
    person_of = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
