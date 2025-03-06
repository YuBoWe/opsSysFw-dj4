from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib import auth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, BasePermission
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from user.serializer import UserSerializers


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers


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
@permission_classes([])
# Create your views here.
def menu_list(request: Request):
    # print('*'*20)
    # print(request.method, request._request.COOKIES, request.headers)
    # print(request.user, request.user.is_authenticated)
    # print('*'*20)
    if request.user.is_superuser:
        pass
    menu_item = []
    i1 = MenuList(mid=1, name="用户管理")
    i2 = MenuList(mid=2, name="资产管理")
    i101 = MenuList(mid=101, name="用户列表", path="users/")
    i102 = MenuList(mid=102, name="角色管理", path="users/roles/")
    i103 = MenuList(mid=103, name="权限管理", path="users/perms/")
    i1.append(i101).append(i102)
    menu_item.extend([i1, i2])

    return Response({
        'default': '101',
        'menulist': menu_item
    })


