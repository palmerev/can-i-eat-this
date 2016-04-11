from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import Food, DietPlan, DietPlanFood
from api.serializers import (FoodSerializer, DietPlanSerializer,
    DietPlanFoodSerializer)


def api_index(request):
    return HttpResponse("Hello, you've reached the API index.")


@csrf_exempt
@api_view(['GET', 'POST'])
def food_list(request):
    """Return all food records owned by the current user"""
    if request.method == 'GET':
        try:
            foods = Food.objects.filter(owner=request.user)
        except TypeError as e:
            print(e.msg)
            return HttpResponse(status=403)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        new_food = Food.objects.create(
            name=request.POST['name'], owner=request.user)
        serializer = FoodSerializer(new_food)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def food_detail(request, pk):
    """Return details for the food with the given pk"""
    if request.method == 'GET':
        try:
            food = Food.objects.get(pk=pk)
        except TypeError as e:
            print(e.msg)
            return HttpResponse(status=403)
        serializer = FoodSerializer(food)
        return Response(serializer.data)


@api_view(['GET'])
def plan_list(request):
    """Return all diet plan records owned by the current user"""
    if request.method == 'GET':
        try:
            plans = DietPlan.objects.filter(owner=request.user)
        except TypeError as e:
            print(e.msg)
            return HttpResponse(status=403)
        serializer = DietPlanSerializer(plans, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def plan_detail(request, pk):
    """Return details for the diet plan with the given pk"""
    if request.method == 'GET':
        try:
            plan = DietPlan.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        serializer = DietPlanSerializer(plan)
        return Response(serializer.data)


@api_view(['GET'])
def food_list_for_plan(request, pk):
    """Return all foods belonging to the diet plan with the given pk"""
    if request.method == 'GET':
        try:
            plan_foods = DietPlanFood.objects.filter(plan=pk)
        except TypeError as e:
            print(e.msg)
            return HttpResponse(status=403)
        serializer = DietPlanFoodSerializer(plan_foods, many=True)
        return Response(serializer.data)
