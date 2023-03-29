import json
import sys
import logging
from django.core.management.base import BaseCommand

from product.models import Product

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Populating User data obtained in JSON from Monolith."

    def handle(self, *args, **options):
        for line in sys.stdin:
            product_data = json.loads(line)
            print("product_data", product_data)

            # Populating User Model
            product = Product(
                title=product_data["title"],
                description=product_data["description"],
                price=product_data["price"],
                link=product_data["link"],
                image=str(product_data["image"]),
                quantity=product_data["quantity"],
            )
            product.save()
