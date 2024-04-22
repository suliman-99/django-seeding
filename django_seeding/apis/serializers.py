from rest_framework import serializers
from django_seeding.models import AppliedSeeder
from django_seeding.seeder_registry import SeederRegistry


class SeedAllSerializer(serializers.Serializer):
    debug = serializers.BooleanField(required=False, allow_null=True)
    ids = serializers.ListField(required=False, allow_null=True, child=serializers.CharField())

    def create(self, validated_data):
        SeederRegistry.import_all_then_seed_all(**validated_data)
        return True


class AppliedSeederSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppliedSeeder
        fields = ('id', )

    def update(self, instance, validated_data):
        instance.delete()
        return AppliedSeeder.objects.create(**validated_data)
