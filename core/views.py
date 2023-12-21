from django.http import HttpResponse
from rest_framework import viewsets,generics,permissions,parsers
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.decorators import action,authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
import cloudinary.uploader
import cloudinary
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
class MyProtectedView(APIView):
    def get(self, request):
        user = request.user

        # Assign roles and permissions to the user based on your logic
        user_roles = user.roles.all()
        user_permissions = Permission.objects.filter(roles__in=user_roles).distinct()

        return Response({
            'user_id': user.id,
            'username': user.username,
            'roles': [role.name for role in user_roles],
            'permissions': [permission.codename for permission in user_permissions],
        }, status=status.HTTP_200_OK)
class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    parser_classes = [parsers.MultiPartParser, ]

    @action(methods=['GET', 'PUT', 'PATCH'], detail=False, url_path='current_user')
    def current_user(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user

        if request.method in ['PUT', 'PATCH']:
            data = request.data.copy()
            data.pop('avatar_user', None)

            serializer = UserSerializers(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                avatar_file = request.data.get('avatar_user')
                if avatar_file:
                    user.avatar_user = avatar_file
                    user.save()

                return Response(UserSerializers(user, context={'request': request}).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serialized_user = UserSerializers(user, context={'request': request}).data
        return Response(serialized_user)



class PostAccommodationViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = PostAccommodation.objects.all()
    serializer_class = PostAccommodationSerializers
    parser_classes = [parsers.MultiPartParser, ]
    @action(methods=['GET'], detail=True)
    def postDetail(self, request, pk):
        house = self.get_object().accommodation
        return Response(Accommodation(house, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class MediaViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

class AccommodationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializers







