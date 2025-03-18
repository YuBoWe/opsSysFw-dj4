from django.urls import path, include
from user.views import menu_list, UserViewSet, PermViewSet, RoleViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('mgr', UserViewSet)
router.register('perm', PermViewSet)
router.register('role', RoleViewSet)

urlpatterns = [
    path('menu/', menu_list),
] + router.urls
print(urlpatterns)
