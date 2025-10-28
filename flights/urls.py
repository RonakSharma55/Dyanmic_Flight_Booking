from django.urls import path
from flights.views.booking_views import book_flight, cancel_booking, booking_history,cities_list,dates_list
from flights.views.flights_views import search_flights,simulate_external_api,get_all_flights
from flights.views import ui_views
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
    

]
