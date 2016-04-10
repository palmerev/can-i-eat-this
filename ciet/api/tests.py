from unittest import skip
from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory, force_authenticate

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
        food = Food.objects.create(owner=self.user, name='Eggs')

        self.assertEqual(food.name, 'Eggs')
        self.assertIs(type(food.date_created), datetime)
        self.assertIs(type(food.date_modified), datetime)

    def test_diet_plan_model(self):
        "Test that DietPlan has the correct fields"
        plan = DietPlan.objects.create(owner=self.user)

        self.assertIs(type(plan.date_created), datetime)
        self.assertIs(type(plan.date_modified), datetime)
        self.assertIs(type(plan.goals), str)
        self.assertIs(type(plan.name), str)

    def test_diet_plan_food_model(self):
        "Test that DietPlanFood has the correct fields and default restrictions"
        food = Food.objects.create(owner=self.user, name='Spam')
        plan = DietPlan.objects.create(owner=self.user)
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
        food = Food.objects.create(owner=self.user, name='Spam')
        plan = DietPlan.objects.create(owner=self.user)
        dp_food = DietPlanFood.objects.create(food=food, plan=plan)
        food_log = FoodLog.objects.create(owner=self.user)

        self.assertIsNotNone(food_log.id)
        self.assertEqual(len(food_log.foods.all()), 0)

        food_log.foods.add(dp_food)
        self.assertEqual(len(food_log.foods.all()), 1)

        self.assertIs(type(food_log.date_created), datetime)
        self.assertEqual(food_log.log, "")


class APIViewGetRequestTestCase(TestCase):
    """Test that views return the expected data for a GET request"""
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(username="evan123")
        self.user2 = User.objects.create_user(username="aaron456")
        self.eggs = Food.objects.create(owner=self.user1, name='Eggs')
        self.cheese = Food.objects.create(owner=self.user1, name='Cheese')
        self.spam = Food.objects.create(owner=self.user1, name='Spam')
        self.peppers = Food.objects.create(owner=self.user2, name='Peppers')
        self.onions = Food.objects.create(owner=self.user2, name='Onions')

    def test_food_list_get(self):
        """Test that food_list GET returns all foods for the user"""
        request = self.factory.get('/api/v1/foods/')
        force_authenticate(request, user=self.user1)
        response = food_list(request)

        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(len(data), 3)
        # DRF Response returns an OrderedDict, convert it to dict to get names
        food_names = [x['name'] for x in data]
        self.assertListEqual(
            [self.eggs.name, self.cheese.name, self.spam.name],
            food_names
        )

    def test_plan_list_get(self):
        """Test that plan_list GET returns all plans for the user"""
        self.plan1 = DietPlan.objects.create(owner=self.user1, name="plan1")
        self.plan2 = DietPlan.objects.create(owner=self.user2, name="plan2")
        request = self.factory.get('/api/v1/dietplans/')
        force_authenticate(request, user=self.user1)
        response = plan_list(request)
        self.assertEqual(len(response.data), 1)
        # print(data)

    def test_plan_list_many_plans_get(self):
        """Test that plan_list GET can return more than one plan for the user"""
        self.plan2 = DietPlan.objects.create(owner=self.user2, name="plan2")
        self.plan3 = DietPlan.objects.create(owner=self.user2, name="plan3")
        request = self.factory.get('/api/v1/dietplans/')
        force_authenticate(request, user=self.user2)
        response = plan_list(request)
        self.assertEqual(len(response.data), 2)
        for plan in response.data:
            self.assertEqual(plan['owner'], self.user2.id)

    def test_food_detail_view_get(self):
        """Test that food_detail GET returns all five fields for food with pk"""
        pk = 1
        request = self.factory.get('api/v1/foods/{}/'.format(pk))
        force_authenticate(request, user=self.user1)
        response = food_detail(request, pk)

        self.assertEqual(len(response.data), 5)  # five fields
        self.assertEqual(response.data['owner'], self.user1.id)
        self.assertEqual(response.data['name'], 'Eggs')

    def test_food_list_for_plan_get(self):
        self.plan1 = DietPlan.objects.create(owner=self.user1, name="plan1")
        self.plan2 = DietPlan.objects.create(owner=self.user1, name="plan2")
        self.plan1_eggs = DietPlanFood.objects.create(
            food=self.eggs, plan=self.plan1)
        self.plan1_cheese = DietPlanFood.objects.create(
            food=self.cheese, plan=self.plan1)
        self.plan1.foods.add(self.plan1_eggs)
        self.plan1.foods.add(self.plan1_cheese)
        pk = self.plan1.id
        request = self.factory.get('/api/v1/dietplans/{}/foods/'.format(pk))
        force_authenticate(request, user=self.user1)
        response = food_list_for_plan(request, pk)
        # print(response.data)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], pk)

        food_names = [x['food']['name'] for x in response.data]
        self.assertListEqual(food_names, ['Eggs', 'Cheese'])


class APIViewPostRequestTestCase(TestCase):
    """Test that views return the expected data for a POST request"""
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(username="evan123")
        self.user2 = User.objects.create_user(username="aaron456")
        self.eggs = Food.objects.create(owner=self.user1, name='Eggs')
        self.cheese = Food.objects.create(owner=self.user1, name='Cheese')
        self.spam = Food.objects.create(owner=self.user1, name='Spam')
        self.peppers = Food.objects.create(owner=self.user2, name='Peppers')
        self.onions = Food.objects.create(owner=self.user2, name='Onions')

    @skip
    def test_food_list_post(self):
        """Test that a new food can be created, and its id returned"""
        pass

    @skip
    def test_food_detail_post(self):
        """Test that food_detail POST returns an error (should be PUT)"""
        pass

    @skip
    def test_plan_list_post(self):
        """Test that a new plan can be created, and its id returned"""
        pass

    @skip
    def test_plan_detail_post(self):
        """Test that plan_detail POST returns an error (should be PUT)"""
        pass

    @skip
    def test_food_list_for_plan_post(self):
        """Test that a food can be added to a plan (creates a DietPlanFood)"""
        pass


class APIViewPutRequestTestCase(TestCase):
    """Test that views return the expected data for a PUT request"""
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(username="evan123")
        self.user2 = User.objects.create_user(username="aaron456")
        self.eggs = Food.objects.create(owner=self.user1, name='Eggs')
        self.cheese = Food.objects.create(owner=self.user1, name='Cheese')
        self.spam = Food.objects.create(owner=self.user1, name='Spam')
        self.peppers = Food.objects.create(owner=self.user2, name='Peppers')
        self.onions = Food.objects.create(owner=self.user2, name='Onions')

    @skip
    def test_food_list_put(self):
        pass
