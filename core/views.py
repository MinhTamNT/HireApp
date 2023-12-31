from rest_framework import viewsets,generics,permissions,parsers
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.decorators import action,authentication_classes, permission_classes
from rest_framework.response import Response
import cloudinary.uploader
import cloudinary


class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    parser_classes = [parsers.MultiPartParser, ]

    @action(methods=['POST'], detail=False, url_path='register')
    def register_user(self, request):
        try:
            data = request.data
            roles_id = data.get('roles')
            roles = Role.objects.filter(id__in=roles_id)
            avatar_file = request.data.get('avatar_user')

            if roles.filter(id__in=[2, 3]).exists() and 'avatar_user' in data:
                if avatar_file:
                    cloudinary_response = cloudinary.uploader.upload(avatar_file)
                    avatar_url = cloudinary_response.get('secure_url')
                else:
                    avatar_url = None

                user = User.objects.create_user(
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    username=data.get('username'),
                    email=data.get('email'),
                    password=data.get('password'),
                    avatar_user=avatar_url
                )

                if user is not None:
                    user.roles.set(roles)
                serializer = UserSerializers(user, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Roles and avatar_user are required for registration."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Role.DoesNotExist:
            return Response({"detail": "Invalid role ID."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Error creating user: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['PUT'], detail=True, url_path='update')
    def updated_user(self, request, pk):
        try:
            user = self.get_object()

            if user != request.user:
                return Response({"detail": "You don't have permission to update this user."},
                                status=status.HTTP_403_FORBIDDEN)

            for field, value in request.data.items():
                setattr(user, field, value)

            # Handle avatar update
            avatar_file = request.data.get('avatar_user')
            if avatar_file:
                cloudinary_response = cloudinary.uploader.upload(avatar_file)
                avatar_public_id = cloudinary_response.get('public_id')
                user.avatar_user = avatar_public_id

            user.save()

            # You may want to serialize and return the updated user
            serializer = UserSerializers(user, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Error updating user: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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







