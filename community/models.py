import binascii
import os

from django.db import models


class Community(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=50, unique=True)
    api_key = models.CharField(max_length=40, unique=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.api_key = binascii.hexlify(os.urandom(20)).decode()

        super().save(args, kwargs)
