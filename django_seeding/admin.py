from django.contrib import admin
from django_seeding.models import AppliedSeeder


@admin.register(AppliedSeeder)
class AppliedSeederAdmin(admin.ModelAdmin):
    list_display = ('id', )
    search_fields = ('id', )
