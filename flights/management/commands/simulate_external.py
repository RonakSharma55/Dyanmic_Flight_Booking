from django.core.management.base import BaseCommand
from flights.external_api.simulator import generate_external_schedules

class Command(BaseCommand):
    help = "Simulate external airline schedules"

    def handle(self, *args, **kwargs):
        generate_external_schedules(days=7)
        self.stdout.write(self.style.SUCCESS("External schedules generated successfully."))
