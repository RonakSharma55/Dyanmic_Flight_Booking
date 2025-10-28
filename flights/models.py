from django.db import models
from django.db import models, transaction
from django.utils.crypto import get_random_string

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



class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('FAILED', 'Failed'),
    ]

    flight = models.ForeignKey('Schedule', on_delete=models.CASCADE, related_name='bookings')
    passenger_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    seat_number = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    pnr = models.CharField(max_length=10, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_pnr(self):
        """Generate a unique PNR"""
        return get_random_string(8).upper()

    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = self.generate_pnr()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pnr} - {self.passenger_name} ({self.status})"
