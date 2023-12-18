from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework import serializers
from .models import *
class UserSerializers(ModelSerializer):
    avatar_user = SerializerMethodField(source='avatar_user')

    def get_avatar_user(self, user):
        if user.avatar_user:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(user.avatar_user.url)
            return user.avatar_user.url  # Return the Cloudinary URL directly

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar_user']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class HouseViewSet(ModelSerializer):
    class Meta:
        model = House
        fields = ['owner','district','city','country','latitude','longitude','contact_number','is_verified',]
class PostAccommodationSerializers(ModelSerializer):
    class Meta:
        model = PostAccommodation
        fields = ['id', 'accommodation', 'user', 'content', 'image_accommodation', 'image_accommodation2', 'image_accommodation3']

    def validate(self, data):
        # Validate that at least one image is provided
        if not any(data.get(f'image_accommodation{i}') for i in range(1, 4)):
            raise serializers.ValidationError("At least one image must be provided.")

        return data

