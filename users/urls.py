from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView)
from .views import UserCreateMixin

router = DefaultRouter()
router.register(
    r'email',
    UserCreateMixin,
    basename='email'
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    )
]
