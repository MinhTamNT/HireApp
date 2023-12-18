from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(House)
admin.site.register(PostAccommodation)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Notification)

# Register your models here.
