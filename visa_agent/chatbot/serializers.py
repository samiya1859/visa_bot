from rest_framework import serializers
from .models import VisaSearch

class VisaSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisaSearch
        fields = ['id', 'country', 'visa_type', 'embassy_url', 
                 'visa_information', 'status', 'created_at']
        read_only_fields = ['embassy_url', 'visa_information', 'status']