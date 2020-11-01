from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import PredictSerializer
from . import models


class GetPredict(generics.CreateAPIView):
    serializer_class = PredictSerializer

    def get_object(self):
        return

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        try:
            u = models.Reader.objects.get(id=user_id) if user_id else models.Reader.objects.get(pk=42880)
        except models.Reader.DoesNotExist:
            return Response({'error': f'Reader with id={user_id} not found'}, status=status.HTTP_404_NOT_FOUND)
        s = self.serializer_class(u)
        return Response(s.data)
