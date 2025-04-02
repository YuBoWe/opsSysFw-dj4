from rest_framework_mongoengine.viewsets import ModelViewSet
from cmdb.models import CiType, Ci
from cmdb.serializers import CiTypSerializer, CiSerializer, CiTypGetFieldSerializer
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.request import Request

from utils.permissions import CRUDdDocumentPermissions


def get_max_version_documents():
    labels = CiType.objects.distinct('label')
    max_version_docs = []

    for label in labels:
        doc = CiType.objects(label=label).order_by('-version').first()
        if doc:
            max_version_docs.append(doc)

    return max_version_docs


class CMDBViewSet(ModelViewSet):
    from rest_framework.permissions import IsAuthenticated
    permission_classes = [IsAuthenticated, CRUDdDocumentPermissions]


class CiViewSet(CMDBViewSet):
    queryset = Ci.objects.all()
    serializer_class = CiSerializer
    # print('~~~'*49)
    # print(Ci.__dict__)
    # print('~~~'*49)

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name:
            qs = qs.filter(name__icontains=name)
        return qs


class CiTypeViewSet(CMDBViewSet):
    queryset = CiType.objects.all()
    serializer_class = CiTypSerializer

    permission_classes = []  # 暂时移除所有权限要求

    def get_serializer_class(self):
        if 'id' in self.kwargs:
            print('`'*40)
            return CiTypGetFieldSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        label = self.request.query_params.get('label', None)
        if label:
            qs = qs.filter(label__icontains=label)
        return qs

    @action(['GET'], detail=False, url_path='getNestFields')
    def get_nest_fields(self, request: Request):
        print('1111111111111111111111111111')
        # print(request.query_params)
        name = request.query_params['name']
        print(name)
        queryset = CiType.objects(name=name).order_by('-version').first()
        serializer = CiTypGetFieldSerializer(queryset)
        return Response(serializer.data)
        # queryset = CiType.objects

    @action(['GET'], detail=False)
    def all_name(self, request: Request):
        queryset = get_max_version_documents()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

# Create your views here.
