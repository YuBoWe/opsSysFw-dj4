from rest_framework_mongoengine.viewsets import ModelViewSet
from cmdb.models import CiType, Ci, ServerInfo
from cmdb.serializers import CiTypSerializer, CiSerializer, CiTypGetFieldSerializer, ServerSerializer
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.request import Request
from utils.permissions import CRUDdDocumentPermissions
from utils.filters import MongoSearchFilter


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


class ServerInfoViewSet(CMDBViewSet):
    queryset = ServerInfo.objects.all()
    serializer_class = ServerSerializer

    @action(['GET'], detail=False)
    def postmachineinfo(self, request: Request):
        # 提交服务器信息
        ip = request.query_params['ipadd_in']
        hostname = request.query_params['hostname']

        queryset = ServerInfo.objects(ipadd_in=ip).first()
        serializer = ServerSerializer(queryset)
        print(serializer.data)
        # id = int(data['id'])
        'update--->'
        # server = Server.objects.get(pk=id)
        # data = get_info(server.in_ip)
        # server.os_version = data['sysinfo']
        # server.host_name = data['host_name']
        # server.os_kernel = data['os_kernel']
        # server.cpu_model = data['cpu']
        # server.cpu_count = data['cpu_count']
        # server.cpu_cores = data['cpu_cores']
        # server.mem = data['mem']
        # server.disk = data['disk']
        # server.status = True
        # server.max_open_files = get_ulimit(server.in_ip)
        # server.uptime = get_uptime(server.in_ip)
        # server.save()
        #
        # # set_service_port(server)  # 设置服务端口信息
        # response.write(json.dumps(u'成功'))
        # return response
        return Response(serializer.data)


class CiViewSet(CMDBViewSet):
    queryset = Ci.objects.all()
    serializer_class = CiSerializer
    # print('~~~'*49)
    # print(Ci.__dict__)
    # print('~~~'*49)
    filter_backends = [MongoSearchFilter]
    mongo_search_fields = ['name__value', 'ci_type', 'Brand__value']

    @action(['PATCH'], detail=True)
    def update_cis(self, request, id):
        print(id)
        instance = self.get_object()
        print('!!!!!!!!!!!!!!!!!!!!')
        print(instance)
        print(request.data)
        request.data.pop('id')
        print(request.data)
        print('!!!!!!!!!!!!!!!!!!!!')
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        #
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
        # return Response()

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     name = self.request.query_params.get('name', None)
    #     if name:
    #         qs = qs.filter(name__icontains=name)
    #     return qs


class CiTypeViewSet(CMDBViewSet):
    queryset = CiType.objects.all()
    serializer_class = CiTypSerializer

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
