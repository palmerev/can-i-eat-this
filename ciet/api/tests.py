from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User

from .views import (food_list, food_detail, plan_list, plan_detail,
    food_list_for_plan)
from .models import Food, DietPlan, DietPlanFood, FoodLog


class APIURLTestCase(TestCase):
    """Test that urls resolve to the correct views"""
    def setUp(self):
        self.prefix = '/api/v1/'

    def tearDown(self):
        del self.prefix

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
    def setUp(self):
        self.user = User.objects.create_user(username="johndoe")

    def test_food_model(self):
        "Test that Food has the correct fields"
        food = Food.objects.create(name='Eggs')

        self.assertEqual(food.name, 'Eggs')
        self.assertIs(type(food.date_created), datetime)
        self.assertIs(type(food.date_modified), datetime)

    def test_diet_plan_model(self):
        "Test that DietPlan has the correct fields"
        plan = DietPlan.objects.create(user=self.user)

        self.assertIs(type(plan.date_created), datetime)
        self.assertIs(type(plan.date_modified), datetime)
        self.assertIs(type(plan.goals), str)
        self.assertIs(type(plan.name), str)

    def test_diet_plan_food_model(self):
        "Test that DietPlanFood has the correct fields and default restrictions"
        food = Food.objects.create(name='Spam')
        plan = DietPlan.objects.create(user=self.user)
        dp_food = DietPlanFood.objects.create(food=food, plan=plan)

        self.assertEqual(dp_food.food.name, 'Spam')
        self.assertEqual(dp_food.plan, plan)
        self.assertEqual(dp_food.status, DietPlanFood.UNASSIGNED)
        self.assertEqual(dp_food.notes, "")

        dp_food.status = DietPlanFood.ALLOWED
        dp_food.save()

        self.assertEqual(dp_food.status, DietPlanFood.ALLOWED)

    def test_food_log_model(self):
        """test that FoodLog has the correct fields"""
        food = Food.objects.create(name='Spam')
        plan = DietPlan.objects.create(user=self.user)
        dp_food = DietPlanFood.objects.create(food=food, plan=plan)
        food_log = FoodLog.objects.create(author=self.user)

        self.assertIsNotNone(food_log.id)
        self.assertEqual(len(food_log.foods.all()), 0)

        food_log.foods.add(dp_food)
        self.assertEqual(len(food_log.foods.all()), 1)

        self.assertIs(type(food_log.date_created), datetime)
        self.assertEqual(food_log.log, "")
