from rest_framework_mongoengine.serializers import DocumentSerializer
from cmdb.models import CiType


class CiTypSerializer(DocumentSerializer):
    class Meta:
        model = CiType
        exclude = ['fields']