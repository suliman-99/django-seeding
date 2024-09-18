from django.db import models


class AppliedSeeder(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self) -> str:
        return self.id
