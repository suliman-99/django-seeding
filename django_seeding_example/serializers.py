from rest_framework import serializers
from django_seeding_example.models import M3, M4, M7


class M3Serializer(serializers.ModelSerializer):
    class Meta:
        model = M3
        fields = ['title', 'description']

    def create(self, validated_data):
        validated_data['title'] = '__' + validated_data['title'] + '__'
        validated_data['description'] = '__' + validated_data['description'] + '__'
        return super().create(validated_data)
    

class M4Serializer(serializers.ModelSerializer):
    class Meta:
        model = M4
        fields = ['title', 'description']

    def create(self, validated_data):
        validated_data['title'] = '__' + validated_data['title'] + '__'
        validated_data['description'] = '__' + validated_data['description'] + '__'
        return super().create(validated_data)
    

class M7Serializer(serializers.ModelSerializer):
    class Meta:
        model = M7
        fields = ['title', 'description']

    def create(self, validated_data):
        validated_data['title'] = '__' + validated_data['title'] + '__'
        validated_data['description'] = '__' + validated_data['description'] + '__'
        return super().create(validated_data)
