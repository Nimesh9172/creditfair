from rest_framework import serializers
from .models import *


class DatauploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataupload
        fields = ["listid"]
        
class LeadDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadDetails
        fields = ["mobile_no","last_dial_no"]


class LeaduploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leadupload
        fields = ["listid"]

class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = "__all__"

class DispositionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = disposition
        fields = ['dispo']

class SubDispositionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = disposition
        fields = ['dispo','sub_dispo']

class AllNumbersSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ['phone_no',"relation"]

class HistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = LogData
        fields = ['sub_disposition','caller_name','remark','contacted_dt']
