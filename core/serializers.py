from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import *

class BaseSerializer(ModelSerializer):
    image = SerializerMethodField(source='image')
    avatar_user = SerializerMethodField(source='avatar_user')
    def get_image(self, accommodation):
        if accommodation.image or accommodation.avatar_user:
            request = self.context.get('request')
            if request:
                return (
                    request.build_absolute_uri(accommodation.image.url) if accommodation.image else None,
                    request.build_absolute_uri(accommodation.avatar_user.url) if accommodation.avatar_user else None
                )
            return accommodation.image.url if accommodation.image else accommodation.avatar_user.url
        return None

    def get_avatar_user(self, accommodation):
        # Check if the instance has the 'avatar_user' attribute
        if accommodation.avatar_user:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(accommodation.avatar_user.url)
            return accommodation.avatar_user.url
        return None


class UserSerializers(BaseSerializer):
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

class HouseSerializres(ModelSerializer):
    class Meta:
        model = House
        fields = ['owner', 'district', 'city', 'country', 'latitude', 'longitude', 'contact_number', 'is_verified']

class MediaSerializer(BaseSerializer):
    class Meta:
        model = Media
        fields = ['image']

class PostAccommodationSerializers(ModelSerializer):
    media = MediaSerializer(many=True)
    class Meta:
        model = PostAccommodation
        fields = ['id', 'accommodation', 'user', 'content', 'media']
