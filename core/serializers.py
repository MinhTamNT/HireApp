from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import *
import cloudinary
from cloudinary.utils import cloudinary_url
class BaseSerializer(ModelSerializer):
    image = SerializerMethodField(source='image')
    def get_image(self, accommodation):
        if accommodation.image :
            request = self.context.get('request')
            if request:
                return (
                    request.build_absolute_uri(accommodation.image.url),
                )
            return accommodation.image.url
        return None
class UserSerializers(ModelSerializer):
    avatar_user = serializers.SerializerMethodField(source='avatar_user')

    def get_avatar_user(self, user):
        if user.avatar_user:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(cloudinary_url(user.avatar_user)[0])
            return cloudinary_url(user.avatar_user)[0]
        return None
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar_user','roles']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class AccommodationSerializers(ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ['owner', 'district', 'city', 'country', 'latitude', 'longitude', 'contact_number', 'is_verified']


class MediaSerializer(BaseSerializer):
    class Meta:
        model = Media
        fields = ['image','post_accomodation']

class PostAccommodationSerializers(ModelSerializer):
    accommodation = AccommodationSerializers(read_only=True)
    class Meta:
        model = PostAccommodation
        fields = ['id', 'accommodation', 'user', 'content',]
