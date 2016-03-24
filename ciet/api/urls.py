from django.conf.urls import url

from . import views

# prefix /api/v1/
app_name = 'api'
urlpatterns = [
    url(r'dietplans/(?P<pk>\d+)/foods/$', views.food_list_for_plan),
    url(r'dietplans/(?P<pk>\d+)/$', views.plan_detail),
    url(r'dietplans/$', views.plan_list),
    url(r'foods/(?P<pk>\d+)/$', views.food_detail),
    url(r'foods/$', views.food_list),
    url(r'', views.api_index),

]
