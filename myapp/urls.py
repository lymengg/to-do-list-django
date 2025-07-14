from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TagViewSet, TaskViewSet

# DRF router for ViewSets
router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('tasks', TaskViewSet)

urlpatterns = [
    # DRF auto-generated API endpoints
    path('api/', include(router.urls)),
]