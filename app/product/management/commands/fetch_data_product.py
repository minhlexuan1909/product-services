import json
import sys
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from product.models import Product


class Command(BaseCommand):
    help = "Extracting product data to JSON format"

    def handle(self, *args, **options):
        # Get product Data from product Model in monolith
        product_microservice_data = Product.objects.all()
        for product_data in product_microservice_data:
            data = {
                "title": product_data.title,
                "description": product_data.description,
                "price": product_data.price,
                "link": product_data.link,
                "image": str(product_data.image),
                "quantity": product_data.quantity,
            }

            # Dumping Data into JSON Format
            json.dump(data, sys.stdout, cls=DjangoJSONEncoder)
            sys.stdout.write("\n")
