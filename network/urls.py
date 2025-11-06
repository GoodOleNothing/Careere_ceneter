from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet, ProductViewSet

app_name = "network"

router = DefaultRouter()
router.register(r'nodes', NetworkNodeViewSet, basename='nodes')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = router.urls
