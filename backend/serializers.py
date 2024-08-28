from rest_framework import serializers
from .models import Instrument,Img_predictions

class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['id', 'name', 'description']

class ImgPredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img_predictions
        fields = '__all__'