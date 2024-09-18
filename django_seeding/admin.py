from django.contrib import admin
from django_seeding.models import AppliedSeeder


@admin.register(AppliedSeeder)
class AppliedSeederAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'created_at',
        'updated_at',
    )
    search_fields = (
        'id',
    )
    ordering = (
        '-updated_at',
    )
