from django.http import HttpResponse
from rest_framework import viewsets,generics,permissions,parsers
from .models import User
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
            serializer = UserSerializers(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serialized_user = UserSerializers(user, context={'request': request}).data
        return Response(serialized_user)



