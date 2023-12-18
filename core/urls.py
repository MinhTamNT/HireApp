from django.urls import path,re_path,include
from .import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register('users',views.UserViewSet)
router.register('post',views.PostAccommodationViewSet)
router.register('house',views.HouseViewSet)
urlpatterns = [
    path('', include(router.urls))
]
