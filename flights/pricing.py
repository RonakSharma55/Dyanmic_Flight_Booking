from datetime import datetime, timezone

def calculate_dynamic_price(schedule, demand_level="medium"):
    """
    Calculate dynamic price for a flight schedule.
    schedule: Schedule object
    demand_level: 'low', 'medium', 'high'
    """
    base_fare = float(schedule.flight.base_fare)
    seats_total = schedule.flight.schedules.first().seats_available + schedule.seats_available
    remaining_pct = schedule.seats_available / seats_total if seats_total > 0 else 0

    # 1️⃣ Adjust based on remaining seats
    if remaining_pct < 0.2:
        price = base_fare * 1.6
    elif remaining_pct < 0.5:
        price = base_fare * 1.25
    else:
        price = base_fare

    # 2️⃣ Adjust based on time until departure
    now = datetime.now(timezone.utc)
    hours_until_departure = (schedule.departure_datetime - now).total_seconds() / 3600

    if hours_until_departure < 48:
        price *= 1.2
    if hours_until_departure < 6:
        price *= 1.5

    # 3️⃣ Adjust based on demand
    demand_multiplier = {"low": 0.95, "medium": 1.0, "high": 1.2}
    price *= demand_multiplier.get(demand_level, 1.0)

    # Round to nearest integer
    return round(price, 2)
