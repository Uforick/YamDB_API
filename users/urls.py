from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CheckEmail, UserCreateMixin, UsersViewSet

router = DefaultRouter()
router.register(
    r'auth/email',
    UserCreateMixin,
    basename='email'
)
router.register('users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'auth/token/',
        CheckEmail,
        name='Check_Email',
    )
]
