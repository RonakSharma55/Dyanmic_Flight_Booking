from rest_framework import serializers
from .models import Flight, Schedule
from .pricing import calculate_dynamic_price


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()  # Nested flight info
    current_price = serializers.SerializerMethodField()
    class Meta:
        model = Schedule
        fields = '__all__'

    def get_current_price(self, obj):
        # For demo, random demand level
        import random
        demand = random.choice(["low", "medium", "high"])
        return calculate_dynamic_price(obj, demand_level=demand)
