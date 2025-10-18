import random
from datetime import datetime, timedelta
from flights.models import Flight, Schedule

AIRLINE_STATUS = ["scheduled", "cancelled", "delayed"]

def generate_external_schedules(days=5):
    """
    Generate random schedules for existing flights
    """
    flights = Flight.objects.all()
    for flight in flights:
        for i in range(days):
            dep_time = datetime.now() + timedelta(days=i, hours=random.randint(5, 20))
            arr_time = dep_time + timedelta(minutes=flight.duration_minutes)
            seats = random.randint(50, 150)
            status = random.choice(AIRLINE_STATUS)
            Schedule.objects.create(
                flight=flight,
                departure_datetime=dep_time,
                arrival_datetime=arr_time,
                seats_available=seats,
                status=status
            )
    print(f"Generated schedules for {len(flights)} flights for {days} days.")
