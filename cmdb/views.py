from rest_framework_mongoengine.viewsets import ModelViewSet
from cmdb.models import CiType
from cmdb.serializers import CiTypSerializer


class CiTypeViewSet(ModelViewSet):
    queryset = CiType.objects.all()
    serializer_class = CiTypSerializer

    permission_classes = []  # 暂时移除所有权限要求

    def get_queryset(self):
        qs = super().get_queryset()
        label = self.request.query_params.get('label', None)
        if label:
            qs = qs.filter(label__icontains=label)
        return qs

# Create your views here.
