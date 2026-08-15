"""
Views для ендпоінтів автентифікації.
Обробляє реєстрацію, вхід, вихід та оновлення токенів.
"""
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth.serializers import RegisterSerializer


class RegisterView(APIView):
    """
        View для реєстрації нового користувача.

        Створює обліковий запис з email, паролем, телефоном та роллю.
        Повертає дані користувача при успішній реєстрації.
        """
    permission_classes = (permissions.AllowAny,)  # Доступно без авторизації

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Registration successful",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "role": user.role.name if user.role else None,
                        "profile": {
                            "name": user.profile.name if user.profile else None,
                        }
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogOutView(APIView):
    """
    View для виходу з системи.
    Додає refresh токен до чорного списку, щоб анулювати його.
    """
    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({
            "message": "Logout successful",
        })
