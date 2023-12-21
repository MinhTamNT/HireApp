from django.urls import path,re_path,include
from .import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register('users',views.UserViewSet)
router.register('post',views.PostAccommodationViewSet)
router.register('accommodation',views.AccommodationViewSet)
router.register('media',views.MediaViewSet)
urlpatterns = [
    path('', include(router.urls))
]
