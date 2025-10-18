from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_flights, name='get_all_flights'),
    path('search/', views.search_flights, name='search_flights'),
    path('simulate/', views.simulate_external_api, name='simulate_external_api'),

]
