from django.urls import path, include
from user.views import menu_list, UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('menu/', menu_list),
] + router.urls
