from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Food, DietPlan
from api.serializers import FoodSerializer, DietPlanSerializer


def api_index(request):
    return HttpResponse("Hello, you've reached the API index.")


@csrf_exempt
@api_view(['GET'])
def food_list(request):
    if request.method == 'GET':
        try:
            foods = Food.objects.filter(owner=request.user)
        except TypeError as e:
            print(e.msg)
            return HttpResponse(status=403)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def food_detail(request):
    pass


@api_view(['GET'])
def plan_list(request):
    if request.method == 'GET':
        try:
            plans = DietPlan.objects.filter(owner=request.user)
        except TypeError as e:
            print(e.msg)
            return HttpResponse(status=403)
        serializer = DietPlanSerializer(plans, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def plan_detail(request):
    pass


@api_view(['GET'])
def food_list_for_plan(request):
    pass
