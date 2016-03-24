from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)


class DietPlan(models.Model):
    pass


class DietPlanFood(models.Model):
    pass


class FoodLog(models.Model):
    pass
