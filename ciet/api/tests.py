from datetime import date

from django.test import TestCase
from django.core.urlresolvers import resolve

from .views import (food_list, food_detail, plan_list, plan_detail,
    food_list_for_plan)
from .models import Food, DietPlan, DietPlanFood, FoodLog


class APIRouteTestCase(TestCase):
    """Test that urls resolve to the correct views"""
    def setUp(self):
        self.prefix = '/api/v1/'

    def test_foods_list_endpoint(self):
        url = self.prefix + 'foods/'
        endpoint = resolve(url)
        self.assertEqual(endpoint.func, food_list)

    def test_foods_detail_endpoint(self):
        url = self.prefix + 'foods/1/'
        endpoint = resolve(url)
        self.assertEqual(endpoint.func, food_detail)

    def test_plan_list_endpoint(self):
        url = self.prefix + 'dietplans/'
        endpoint = resolve(url)
        self.assertEqual(endpoint.func, plan_list)

    def test_plan_detail_endpoint(self):
        url = self.prefix + 'dietplans/1/'
        endpoint = resolve(url)
        self.assertEqual(endpoint.func, plan_detail)

    def test_food_list_for_plan_endpoint(self):
        url = self.prefix + 'dietplans/1/foods/'
        endpoint = resolve(url)
        self.assertEqual(endpoint.func, food_list_for_plan)


class APIModelTestCase(TestCase):
    """Test that models have the right fields"""
    def test_food_model(self):
        food = Food.objects.create(name='Eggs')
        self.assertEqual(food.name, 'Eggs')
        self.assertIs(type(food.date_created), date)
        self.assertIs(type(food.date_modified), date)
