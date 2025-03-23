from django.urls import path
from rest_framework_mongoengine.routers import SimpleRouter
from .views import CiTypeViewSet

router = SimpleRouter()
router.register('citypes', CiTypeViewSet)

urlpatterns = [] + router.urls
