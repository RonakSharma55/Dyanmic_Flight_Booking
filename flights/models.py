from django.db import models

class Flight(models.Model):
    airline = models.CharField(max_length=100)
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    duration_minutes = models.PositiveIntegerField()
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.airline} ({self.origin} → {self.destination})"
    
class Schedule(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="schedules")
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    seats_available = models.IntegerField(default=100)
    status = models.CharField(max_length=20, default="scheduled")

    def __str__(self):
        return f"{self.flight.airline} {self.flight.origin}->{self.flight.destination} at {self.departure_datetime}"
