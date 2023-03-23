from rest_framework import serializers
from .models import *


class DatauploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataupload
        fields = ["listid"]
