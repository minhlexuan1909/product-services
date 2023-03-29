import json
import sys
import logging
from django.core.management.base import BaseCommand

from tag.models import Tag

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Populating User data obtained in JSON from Monolith."

    def handle(self, *args, **options):
        for line in sys.stdin:
            tag_data = json.loads(line)

            # Populating User Model
            tag = Tag(
                name=tag_data["name"],
                description=tag_data["description"],
            )
            tag.save()
