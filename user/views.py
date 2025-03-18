from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.models import Permission, ContentType, Group
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAdminUser, BasePermission, IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth import get_user_model
from user.serializer import UserSerializers, PermSerializers, RoleSerializer
from django.http.response import Http404
from .models import UserProfile
from utils.exception import InvalidPassword
from rest_framework import filters

_exclude_contenttypes = [c.id for c in ContentType.objects.filter(model__in=
[
    'logentry', 'group', 'permission',
    'contenttype', 'session'
])]


class RoleViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(['GET'], detail=True, url_path='perms')
    def perms(self, request, pk=None):
        instance = self.get_object()
        data = RoleSerializer(instance).data
        data['allPerms'] = list(PermViewSet.queryset.values('id', 'name'))
        return Response(data)


class PermViewSet(ModelViewSet):
    queryset = Permission.objects.exclude(content_type__in=_exclude_contenttypes)
    serializer_class = PermSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'codename']


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers

    def partial_update(self, request, *args, **kwargs):
        request.data.pop('username', None)
        request.data.pop('id', None)
        request.data.pop('password', None)
        request.data.pop('is_superuser', None)
        return super().partial_update(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(username__icontains=username)
        return qs

    def get_object(self):
        if self.request.method.lower() != 'get':
            pk = self.kwargs.get('pk')
            if pk == 1 or pk == '1':
                print('禁止操作管理员')
                raise Http404
        return super().get_object()

    @action(['GET'], detail=False, url_path='whoami')
    def whoami(self, request):
        print(request.user)
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username
            }
        })

    @action(['POST'], detail=True, url_path='setpwd')
    def setpwd(self, request, pk):
        if int(pk) != request.user.id:
            raise Http404
        user: UserProfile = self.get_object()
        if user.check_password(request.data['oldpass']):
            user.set_password(request.data['newpass'])
            user.save()
            return Response()
        raise InvalidPassword

    @action(['POST'], detail=True, url_path='setuserspwd')
    def setuserspwd(self, request, pk):
        user: UserProfile = self.get_object()
        user.set_password(request.data['newpass'])
        user.save()
        return Response()

    @action(['GET'], detail=True, url_path='role')
    def role(self, request, pk):
        instance = self.get_object()
        data = UserSerializers(instance).data
        data['roles'] = [r.get('id') for r in instance.groups.values('id')]
        data['allRoles'] = list(Group.objects.values('id', 'name'))
        return Response(data)

    @role.mapping.put  # /users/mgr/2/roles/ PUT
    def set_roles(self, request, pk=None):
        instance = self.get_object()
        roles = request.data.get('roles', [])
        instance.groups.set(roles)
        return Response(status=201)


class IsSuperUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class MenuList(dict):
    def __init__(self, mid, name, path=None):
        super().__init__()
        self["id"] = mid
        self["name"] = name
        self.__setitem__('path', path)
        self['children'] = []

    def append(self, value):
        self["children"].append(value)
        return self


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# Create your views here.
def menu_list(request: Request):
    # print('*'*20)
    # print(request.method, request._request.COOKIES, request.headers)
    # print(request.user, request.user.is_authenticated)
    # print('*'*20)
    menu_item = []

    i2 = MenuList(mid=2, name="资产管理")
    if request.user.is_superuser:
        i1 = MenuList(mid=1, name="用户管理")
        i101 = MenuList(mid=101, name="用户列表", path="users/")
        i102 = MenuList(mid=102, name="角色管理", path="users/roles/")
        i103 = MenuList(mid=103, name="权限列表", path="users/perms/")
        i1.append(i101).append(i102).append(i103)
        menu_item.append(i1)
    menu_item.append(i2)
    return Response({
        'default': '101',
        'menulist': menu_item
    })


