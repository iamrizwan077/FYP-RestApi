from myapp import models
from rest_framework import serializers

class NTNSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.NTN
        fields = '__all__' 


class AnomalySerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.Anomaly
        fields = '__all__' 


class MissingInvoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=models.MissingInvoice
        fields = '__all__' 