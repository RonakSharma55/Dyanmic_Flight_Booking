from django.core.management.base import BaseCommand
from flights.models import Schedule
import random

class Command(BaseCommand):
    help = "Simulate demand and availability changes for schedules"

    def handle(self, *args, **kwargs):
        schedules = Schedule.objects.all()
        for sched in schedules:
            # Randomly change seats available (simulate bookings/cancellations)
            delta = random.randint(-5, 5)  # +/- seats
            new_seats = max(0, sched.seats_available + delta)
            sched.seats_available = new_seats

            # Optionally update status (e.g., delayed/cancelled)
            sched.status = random.choices(
                ["scheduled", "cancelled", "delayed"],
                weights=[80, 10, 10],
                k=1
            )[0]

            sched.save()

        self.stdout.write(self.style.SUCCESS(f"Simulated demand and availability for {schedules.count()} schedules."))
