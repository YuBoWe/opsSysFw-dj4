from django.urls import path
from rest_framework_mongoengine.routers import SimpleRouter
from .views import CiTypeViewSet, CiViewSet

router = SimpleRouter()
router.register('citypes', CiTypeViewSet)
router.register('cis', CiViewSet)

urlpatterns = [] + router.urls
print('!'*30)
print(urlpatterns)
print("!" * 30)
