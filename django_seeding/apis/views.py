from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django_seeding.models import AppliedSeeder
from django_seeding.seeder_registry import SeederRegistry
from django_seeding.apis.serializers import AppliedSeederSerializer, SeedAllSerializer


class RegisteredSeederViewSet(ListModelMixin, GenericViewSet):
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        SeederRegistry.import_all()
        return Response([seeder._get_id() for seeder in SeederRegistry.seeders])
    
    @action(detail=False, methods=['post'], url_path='seed-all')
    def seed_all(self, request, *args, **kwargs):
        serializer = SeedAllSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class AppliedSeederViewSet(ModelViewSet):
    queryset = AppliedSeeder.objects.all()
    serializer_class = AppliedSeederSerializer
    
    @action(detail=False, methods=['delete'], url_path='delete-all')
    def delete_all(self, request, *args, **kwargs):
        AppliedSeeder.objects.all().delete()
        return Response({})
