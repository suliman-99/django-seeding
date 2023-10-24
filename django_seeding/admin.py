from django.contrib import admin
from .models import AppliedSeeder


@admin.register(AppliedSeeder)
class AppliedSeederAdmin(admin.ModelAdmin):
    pass
