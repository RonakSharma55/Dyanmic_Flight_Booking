from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.utils import timezone
from django.db.models import F
from flights.models import Schedule  # uses your Schedule model with FK to Flight
from flights.pricing import calculate_dynamic_price
import datetime

BASE_URL = "http://127.0.0.1:8000/api"  # Django backend runs here

def home_page(request):
    # Fetch dropdown data from backend APIs
    cities_response = requests.get(f"{BASE_URL}/cities/")
    dates_response = requests.get(f"{BASE_URL}/flights/dates/")

    cities = cities_response.json() if cities_response.status_code == 200 else []
    dates = dates_response.json() if dates_response.status_code == 200 else []

    # If user searched flights
    results = []
    if request.method == "GET" and 'origin' in request.GET:
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        date = request.GET.get('date')
        url = f"{BASE_URL}/flights/search/?origin={origin}&destination={destination}&date={date}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()

    return render(request, 'home.html', {
        'cities': cities,
        'dates': dates,
        'results': results
    })

def _format_time(dt):
    return dt.strftime("%H:%M") if dt else ""

def search_results(request):
    """
    Render a Skyscanner-like search results page.
    Query params: ?origin=XXX&destination=YYY&date=YYYY-MM-DD
    """
    origin = request.GET.get("origin", "")
    destination = request.GET.get("destination", "")
    date_str = request.GET.get("date", "")

    flights_data = []
    date_options = []

    # build a few date tabs (3 before -> 3 after) if date provided, otherwise next 7 days
    try:
        if date_str:
            base = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            base = datetime.date.today()
    except Exception:
        base = datetime.date.today()

    date_options = [(base + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(-3, 4)]

    # Query DB for schedules matching origin/destination/date
    if origin and destination and date_str:
        # Schedule has departure_datetime: filter by date portion
        schedules = Schedule.objects.filter(
            flight__origin__iexact=origin,
            flight__destination__iexact=destination,
            departure_datetime__date=date_str
        ).select_related("flight").order_by("departure_datetime")

        for s in schedules:
            # determine demand level (if you store demand_factor) otherwise 'medium'
            demand = getattr(s, "demand_factor", None)
            if demand is None:
                demand_level = "medium"
            else:
                try:
                    d = float(demand)
                    if d >= 1.15:
                        demand_level = "high"
                    elif d >= 0.9:
                        demand_level = "medium"
                    else:
                        demand_level = "low"
                except Exception:
                    demand_level = "medium"

            price = calculate_dynamic_price(s, demand_level=demand_level)
            flights_data.append({
                "id": s.id,
                "airline": s.flight.airline,
                "origin": s.flight.origin,
                "destination": s.flight.destination,
                "departure_time": _format_time(s.departure_datetime),
                "arrival_time": _format_time(s.arrival_datetime),
                "duration": s.flight.duration_minutes if s.flight else "",
                "stops": 0,  # adapt if you model stops
                "baggage": "Cabin only",  # placeholder, extend if you have baggage data
                "price": price,
                "seats_available": getattr(s, "seats_available", None),
            })

    context = {
        "flights": flights_data,
        "origin": origin,
        "destination": destination,
        "date": date_str if date_str else base.strftime("%Y-%m-%d"),
        "date_options": date_options,
    }
    return render(request, "search_results.html", context)





def booking_page(request):
    return render(request, "booking.html")
