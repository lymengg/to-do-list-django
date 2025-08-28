from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import CategoryViewSet, TagViewSet, TaskViewSet, NoteViewSet

# DRF router for ViewSets
router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('tasks', TaskViewSet)

nested_router = NestedDefaultRouter(router, 'tasks', lookup='task')
nested_router.register('notes', NoteViewSet, basename='task-notes')

urlpatterns = [
    # DRF auto-generated API endpoints
    path('api/', include(router.urls)),
    path('api/', include(nested_router.urls)),
]