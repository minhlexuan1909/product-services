from django.db import models


class Tag(models.Model):
    """Tag for filtering products"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
