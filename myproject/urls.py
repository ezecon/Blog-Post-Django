from django.urls import path
from .views import PredictDiseaseView

urlpatterns = [
    path('predict-disease/', PredictDiseaseView.as_view(), name='predict_disease'),
]
