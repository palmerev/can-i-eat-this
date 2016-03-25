from rest_framework import serializers
from .models import Food, DietPlan, DietPlanFood


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = ('id', 'name', 'date_created', 'date_modified')
