from django.contrib.auth.models import User

from rest_framework import serializers
from .models import Food, DietPlan, DietPlanFood


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'owner', 'name', 'date_created', 'date_modified')


class DietPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlan
        fields = (
            'id', 'owner', 'name', 'date_created', 'date_modified', 'goals')


class DietPlanFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlanFood
        fields = ('id', 'food', 'plan', 'status', 'notes')
        depth = 1
