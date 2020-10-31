from django.urls import path
from .views import GetPredict

urlpatterns = [
    path(r'get_preds/', GetPredict.as_view()),
]
