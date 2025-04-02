from rest_framework_mongoengine.serializers import DocumentSerializer, DynamicDocumentSerializer
from cmdb.models import CiType, Ci
from .models import CiTypeField


class CiTypGetFieldSerializer(DocumentSerializer):
    class Meta:
        model = CiType
        fields = '__all__'


class CiTypSerializer(DocumentSerializer):
    class Meta:
        model = CiType
        exclude = ['fields']


class CiSerializer(DynamicDocumentSerializer):
    class Meta:
        model = Ci
        fields = '__all__'

