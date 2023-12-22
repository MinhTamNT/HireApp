from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
class Role(models.Model):
    ADMIN = 1
    HOST = 2
    TENANT = 3
    ROLE_CHOICES = (
        (TENANT, 'TENANT'),
        (HOST, 'HOST'),
        (ADMIN, 'admin'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()
class User(AbstractUser, BaseModel):
    roles = models.ManyToManyField(Role,name='roles',related_name='role')
    avatar_user = CloudinaryField("avatar_user")
    follow = models.ManyToManyField("Follow", related_name='followers')


class Accommodation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    contact_number = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False, choices=[(True, 'Verified'), (False, 'Not Verified')])

    def __str__(self):
        return self.district

class PostAccommodation(BaseModel):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


    def __str__(self):
        return f"Post {self.id} - Accommodation {self.accommodation.id}"


class Media(models.Model):
    name = models.CharField(max_length=255,null=True)
    image = CloudinaryField("image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_accomodation = models.ForeignKey(PostAccommodation, on_delete=models.CASCADE, related_name='post', null=True)

    def __str__(self):
        return self.name or "No Name"


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set', related_query_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set', related_query_name='followers')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.content}"
