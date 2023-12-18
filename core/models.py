from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from cloudinary.models import CloudinaryField
# Create your models here.
class BaseModel(models.Model):
    update_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        ('host', 'Host Accommodation'),
        ('admin', 'Administrators Accommodation'),
        ('tenant', 'Tenant'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')
    avatar_user = CloudinaryField('image')


class House(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    contact_number = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)



class PostAccommodation(BaseModel):
    accommodation = models.ForeignKey(House, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image_accommodation = CloudinaryField('image',null=True)
    image_accommodation2 = CloudinaryField('image',null=True)
    image_accommodation3 = CloudinaryField('image',null=True)


    def __str__(self):
        return f"Post {self.id} - Accommodation {self.accommodation.id}"
class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.content}"

