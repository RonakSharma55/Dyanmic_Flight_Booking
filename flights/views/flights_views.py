from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from flights.models import Flight, Schedule
from flights.pricing import calculate_dynamic_price
import random
from flights.serializers import FlightSerializer, ScheduleSerializer
from flights.external_api.simulator import generate_external_schedules
@api_view(['GET'])
def get_all_flights(request):
    flights = Flight.objects.all()
    serializer = FlightSerializer(flights, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def search_flights(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    date_str = request.GET.get('date')
    sort_by = request.GET.get('sort', 'price')
    order = request.GET.get('order', 'asc')

    # Input validation
    if not origin or not destination or not date_str:
        return Response({"error": "origin, destination, and date are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Date format check
    try:
        search_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    # Filter schedules
    schedules = Schedule.objects.filter(
        flight__origin__iexact=origin,
        flight__destination__iexact=destination,
        departure_datetime__date=search_date
    )

    # Annotate dynamic price
    schedules_with_price = []
    for sched in schedules:
        demand = random.choice(["low", "medium", "high"])  # Simulate demand
        sched.current_price = calculate_dynamic_price(sched, demand_level=demand)
        schedules_with_price.append(sched)

    # Sorting
    if sort_by == 'duration':
        schedules_with_price.sort(key=lambda x: x.flight.duration_minutes, reverse=(order=="desc"))
    else:  # sort by price
        schedules_with_price.sort(key=lambda x: x.current_price, reverse=(order=="desc"))

    serializer = ScheduleSerializer(schedules_with_price, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def simulate_external_api(request):
    generate_external_schedules(days=7)
    return Response({"status": "success", "message": "External schedules generated"})