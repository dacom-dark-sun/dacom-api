from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=300, null=True, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def create_with_wallet(self):
        pass
