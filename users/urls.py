from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import check_email, UserCreateMixin, UsersViewSet

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
        check_email,
        name='Check_Email',
    )
]
