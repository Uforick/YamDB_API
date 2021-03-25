from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoriesViewSet, GengresViewSet, TitlesViewSet

router_v1 = SimpleRouter()

router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GengresViewSet)
router_v1.register('titles', TitlesViewSet)

urlpatterns = [
    path('v1/users/', include('users.urls')),
    path('v1/', include(router_v1.urls)),
]
