from django.urls import path, include
from user.views import menu_list, UserViewSet, PermViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('mgr', UserViewSet)
router.register('perm', PermViewSet)

urlpatterns = [
    path('menu/', menu_list),
] + router.urls
print(urlpatterns)
