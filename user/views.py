from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from djoser import signals
from djoser.conf import settings


class UserViewSet(DjoserUserViewSet):

    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),

        }

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [user.email]
            settings.EMAIL.confirmation(self.request, context).send(to)

        return Response(data, status=status.HTTP_204_NO_CONTENT)
