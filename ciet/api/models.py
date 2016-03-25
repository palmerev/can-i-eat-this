from django.db import models
from django.conf import settings


class Food(models.Model):
    """A generic food"""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class DietPlan(models.Model):
    """A user-specific diet plan"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    goals = models.CharField(max_length=255, blank=True)


class DietPlanFood(models.Model):
    """A food on a specific diet plan, including the food's restrictions"""
    ALLOWED, NOT_ALLOWED, RESTRICTED, UNASSIGNED = 1, 2, 3, 0
    FOOD_RESTRICTIONS = (
        (ALLOWED, 'Allowed'),
        (NOT_ALLOWED, 'Not Allowed'),
        (RESTRICTED, 'Restricted'),
        (UNASSIGNED, 'Unassigned'))
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        choices=FOOD_RESTRICTIONS, default=UNASSIGNED)
    notes = models.CharField(max_length=255, blank=True)


class FoodLog(models.Model):
    """A user's food log associated with a diet plan, including foods eaten"""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    foods = models.ManyToManyField(DietPlanFood, related_name='logs')
    date_created = models.DateTimeField(auto_now_add=True)
    log = models.TextField(blank=True)
