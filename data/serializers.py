from rest_framework import serializers
from . import models
from ml import get_predict


class PredictSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = models.Reader
        fields = ('books',)

    @staticmethod
    def get_books(user: models.Reader):
        book_ids = get_predict.get_top_books(user.id)
        books = models.Catalog.objects.filter(id__in=book_ids)
        return BookSerializer(books, many=True)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Catalog
        fields = ('title', 'author', 'publisher')
