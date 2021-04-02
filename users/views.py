import secrets
import string

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.views import AllYouUsuallyNeedViewSet

from . import permissions, serializers
from .models import CustomUser as User


def generate_alphanum_crypt_string():
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(12))
    return(crypt_rand_string)


class UserCreateMixin(CreateModelMixin, GenericViewSet):
    serializer_class = serializers.EmailForTokenSerialzer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        validatedData = serializer.validated_data
        email = validatedData.get('email')
        confirmation_code = generate_alphanum_crypt_string()
        confirmation_code_hashers = make_password(confirmation_code)
        send_mail(
            'Код подтверждения email',
            confirmation_code,
            settings.CORE_EMAIL_ADRESS,
            [email],
            fail_silently=False,
        )
        serializer.save(
            confirmation_code=confirmation_code,
            password=confirmation_code_hashers,
            email=email, username=email,
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def check_email(request):
    serializer = serializers.EmailConfermeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        confirmation_code = serializer.validated_data['confirmation_code']
    check_user = get_object_or_404(User, email=email)
    if check_user.confirmation_code == confirmation_code:
        create_token = RefreshToken.for_user(check_user)
        token = str(create_token.access_token)
        return Response({'token': token})
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(
    AllYouUsuallyNeedViewSet,
    RetrieveModelMixin,
    UpdateModelMixin
):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminOnly]
    lookup_field = 'username'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']

    def perform_update(self, serializer):
        serializer.save()

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        me = get_object_or_404(User, username=request.user.username)
        serializer = serializers.MeSerializer(me, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(data=request.data)

        return Response(serializer.data)
