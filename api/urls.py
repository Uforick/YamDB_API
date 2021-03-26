from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoriesViewSet,
    GengresViewSet,
    TitlesViewSet,
    UsersViewSet,
    # MeViewSet
)

router_v1 = SimpleRouter()

router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GengresViewSet)
router_v1.register('titles', TitlesViewSet)
# router_v1.register('users/me', MeViewSet, basename='me')
router_v1.register('users', UsersViewSet)


urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(router_v1.urls)),
]
