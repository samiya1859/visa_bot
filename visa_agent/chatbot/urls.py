from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisaSearchViewSet

router = DefaultRouter()
router.register(r'visa-search', VisaSearchViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]