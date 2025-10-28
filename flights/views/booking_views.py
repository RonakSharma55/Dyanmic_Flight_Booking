from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from flights.models import Schedule, Booking
from random import choice
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from flights.models import Booking
from django.http import JsonResponse
import json

from rest_framework.decorators import api_view
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from flights.models import Booking

from django.http import FileResponse, Http404
import os




def download_receipt(request, pnr):
    try:
        booking = Booking.objects.select_related("flight__flight").get(pnr=pnr)
    except Booking.DoesNotExist:
        raise Http404("Invalid PNR.")

    schedule = booking.flight  # Schedule object
    flight = schedule.flight   # Flight object

    # Make sure media folder exists
    receipt_dir = "media/receipts"
    os.makedirs(receipt_dir, exist_ok=True)
    file_path = os.path.join(receipt_dir, f"receipt_{pnr}.pdf")

    # 🧾 Generate the PDF if not already saved
    if not os.path.exists(file_path):
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 18)
        c.drawString(200, height - 100, "✈️ Flight Booking Receipt")

        c.setFont("Helvetica", 12)
        y = height - 150

        info = [
            ("PNR:", booking.pnr),
            ("Passenger Name:", booking.passenger_name),
            ("Email:", booking.passenger_email),
            ("Airline:", flight.airline),
            ("Route:", f"{flight.origin} → {flight.destination}"),
            ("Departure Time:", str(schedule.departure_datetime)),
            ("Arrival Time:", str(schedule.arrival_datetime)),
            ("Seat Number:", booking.seat_number),
            ("Price:", f"₹{booking.price}"),
            ("Status:", booking.status),
        ]

        for label, value in info:
            c.drawString(70, y, f"{label} {value}")
            y -= 25

        c.line(70, y - 10, 500, y - 10)
        c.drawString(70, y - 40, "Thank you for booking with Flight Booking Simulator!")
        c.save()

    return FileResponse(open(file_path, "rb"), content_type="application/pdf")

@api_view(["POST"])
def book_flight(request):
    """
    Multi-step booking flow:
    1. Select flight + seat
    2. Submit passenger info
    3. Simulate payment (success/fail)
    4. Generate PNR if success
    """
    try:
        with transaction.atomic():  # Ensures concurrency-safe booking
            schedule_id = request.data.get("schedule_id")
            passenger_name = request.data.get("passenger_name")
            passenger_email = request.data.get("passenger_email")
            seat_number = request.data.get("seat_number")
            price = request.data.get("price")

            if not all([schedule_id, passenger_name, passenger_email, seat_number, price]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            schedule = get_object_or_404(Schedule, id=schedule_id)

            # Check if seat already booked
            if Booking.objects.filter(flight=schedule, seat_number=seat_number, status='CONFIRMED').exists():
                return Response({"error": "Seat already booked"}, status=status.HTTP_409_CONFLICT)

            # Step 1: Create pending booking
            booking = Booking.objects.create(
                flight=schedule,
                passenger_name=passenger_name,
                passenger_email=passenger_email,
                seat_number=seat_number,
                price=price,
                status='PENDING'
            )

            # Step 2: Simulate payment
            payment_result = "SUCCESS" 
            if payment_result == "SUCCESS":
                booking.status = "CONFIRMED"
                booking.save()
                message = f"Booking Confirmed ✅ | PNR: {booking.pnr}"
            else:
                booking.status = "FAILED"
                booking.save()
                message = "Payment Failed ❌ Booking not confirmed."

            return Response({
                "pnr": booking.pnr,
                "status": booking.status,
                "message": message
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
def cancel_booking(request):
    """
    Cancel a booking by PNR.
    """
    pnr = request.data.get("pnr")
    passenger_email = request.data.get("passenger_email")

    if not pnr or not passenger_email:
        return Response({"error": "PNR and passenger email required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        booking = Booking.objects.get(pnr=pnr, passenger_email=passenger_email)
        if booking.status != "CONFIRMED":
            return Response({"error": f"Cannot cancel booking with status {booking.status}"}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = "CANCELLED"
        booking.save()
        return Response({"message": f"Booking {pnr} cancelled successfully ✅"}, status=status.HTTP_200_OK)

    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def booking_history(request):
    """
    Retrieve all bookings for a passenger by email.
    """
    passenger_email = request.query_params.get("passenger_email")
    if not passenger_email:
        return Response({"error": "Passenger email required"}, status=status.HTTP_400_BAD_REQUEST)

    bookings = Booking.objects.filter(passenger_email=passenger_email).order_by("-created_at")
    history = [
        {
            "pnr": b.pnr,
            "flight_id": b.flight.id,
            "seat_number": b.seat_number,
            "status": b.status,
            "price": b.price,
            "created_at": b.created_at
        } for b in bookings
    ]
    return Response({"history": history}, status=status.HTTP_200_OK)


# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from flights.models import Flight

@api_view(['GET'])
def cities_list(request):
    origin_cities = Flight.objects.values_list('origin', flat=True).distinct()
    destination_cities = Flight.objects.values_list('destination', flat=True).distinct()
    all_cities = sorted(set(origin_cities) | set(destination_cities))
    return Response(all_cities)




def dates_list(request):
    # Get all distinct departure dates
    dates = Schedule.objects.values_list('departure_datetime', flat=True).distinct()
    # Format as YYYY-MM-DD
    formatted_dates = sorted({dt.date().isoformat() for dt in dates})
    return JsonResponse(formatted_dates, safe=False)

