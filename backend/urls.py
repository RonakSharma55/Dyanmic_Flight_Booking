"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from flights.views import ui_views
def home(request):
    return HttpResponse("Welcome to Flight Booking Simulator API!")


from django.urls import path
from flights.views.booking_views import book_flight, cancel_booking, booking_history,cities_list,dates_list
from flights.views.flights_views import search_flights,simulate_external_api,get_all_flights
from flights.views import ui_views
from flights.views.booking_views import download_receipt
urlpatterns = [
    path('', ui_views.home_page, name='home'),

    # ✈️ API Routes
    path('api/flights/', get_all_flights, name='get_all_flights'),
    path('api/flights/search/', search_flights, name='search_flights'),
    path('api/flights/simulate/', simulate_external_api, name='simulate_external_api'),

    # 🧾 Booking APIs
    path('api/book/', book_flight, name='book_flight'),
    path('api/cancel/', cancel_booking, name='cancel_booking'),
    path('api/history/', booking_history, name='booking_history'),

    # 📅 Dropdown APIs for UI
    path('api/cities/', cities_list, name='cities_list'),
    path('api/flights/dates/', dates_list, name='dates_list'),
    path('admin/', admin.site.urls),
    path('search/results/', ui_views.search_results, name='search_results'),
    path('booking/', ui_views.booking_page, name='booking_page'),
    path('api/bookings/receipt/<str:pnr>/', download_receipt, name='download_receipt'),

]

