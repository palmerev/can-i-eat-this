from django.shortcuts import render
from django.http import HttpResponse


def api_index(request):
    return HttpResponse("Hello, you've reached the API index.")


def food_list(request):
    pass


def food_detail(request):
    pass


def plan_list(request):
    pass


def plan_detail(request):
    pass


def food_list_for_plan(request):
    pass
