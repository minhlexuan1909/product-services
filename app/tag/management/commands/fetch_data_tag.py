import json
import sys
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from product.models import Tag


class Command(BaseCommand):
    help = "Extracting tag data to JSON format"

    def handle(self, *args, **options):
        # Get tag Data from tag Model in monolith
        tag_microservice_data = Tag.objects.all()
        for tag_data in tag_microservice_data:
            data = {
                "name": tag_data.name,
                "description": tag_data.description,
            }

            # Dumping Data into JSON Format
            json.dump(data, sys.stdout, cls=DjangoJSONEncoder)
            sys.stdout.write("\n")
