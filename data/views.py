from rest_framework import generics
from .serializers import PredictSerializer


class GetPredict(generics.RetrieveAPIView):
    serializer_class = PredictSerializer

    def get_object(self):
        pass
