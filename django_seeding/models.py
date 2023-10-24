from django.db import models


class AppliedSeeder(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    def __str__(self) -> str:
        return self.id
