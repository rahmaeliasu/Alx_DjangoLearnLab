from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserDetailSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Endpoint for user profile management.
    GET: Retrieve your own profile.
    PUT/PATCH: Update your bio or profile picture.
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Return the token and user data in the response
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "email": user.email
        }, status=status.HTTP_201_CREATED)

# Custom Login View (Extending ObtainAuthToken)
# This allows us to return more than just the token (e.g., user ID, email)
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })

# Logout View
class LogoutView(APIView):
    def post(self, request):
        # Simply delete the token to force login again
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
