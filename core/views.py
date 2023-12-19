from django.http import HttpResponse
from rest_framework import viewsets,generics,permissions,parsers
from .models import User,PostAccommodation
from .serializers import *
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
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
class PostAccommodationViewSet(viewsets.ViewSet,generics.ListAPIView,generics.CreateAPIView,generics.RetrieveAPIView):
    queryset = PostAccommodation.objects.all()
    serializer_class = PostAccommodationSerializers
    parser_classes = [parsers.MultiPartParser, ]
    @action(methods=['GET'],detail=True)
    def postDetail(self,request,pk):
        house = self.get_object().house_set.objects.all()
        return Response(HouseSerializres(house,many=True,context={'request':request}).data,status=status.HTTP_200_OK)
class HouseViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializres





