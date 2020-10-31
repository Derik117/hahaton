from rest_framework import serializers
from . import models
from ml import get_predict


class PredictSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()

    class Meta:
        model = models.Reader
        fields = ('books', 'events', 'services')

    @staticmethod
    def get_books(user: models.Reader):
        book_ids = get_predict.get_top_books(user.id if user else None)
        books = models.Catalog.objects.filter(id__in=book_ids)
        return BookSerializer(books, many=True).data

    @staticmethod
    def get_events(user: models.Reader):
        event_ids = get_predict.get_top_events(user.id if user else None)
        events = models.Event.objects.filter(id__in=event_ids)
        return EventSerializer(events, many=True).data

    @staticmethod
    def get_services(user: models.Reader):
        service_ids = get_predict.get_top_services(user.id if user else None)
        services = models.Service.objects.filter(id__in=service_ids).prefetch_related(
            'organization', 'service_class'
        )
        return ServiceSerializer(services, many=True).data


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Catalog
        fields = ('id', 'title', 'author', 'publisher', 'cover_url', 'year', 'age_rating')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ('id', 'name', 'status', 'start_date', 'end_date', 'description', 'address', 'age_limit', 'age_group')


class ServiceSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.short_name')
    organization_street_name = serializers.CharField(source='organization.street_name')
    organization_underground_name = serializers.CharField(source='organization.underground_name')
    service_class_name = serializers.CharField(source='service_class.name')

    class Meta:
        model = models.Service
        fields = ('id', 'finance_type', 'schedule_type', 'service_name', 'duration', 'duration_unit',
                  'organization_name', 'organization_street_name', 'organization_underground_name',
                  'service_class_name')
