from django.urls import path
from .views import edit_profile, user_change_profile_picture, subscription
urlpatterns = [
    path("edit/", edit_profile, name="edit_profile"),
    path('change-profile-picture/', user_change_profile_picture, name='user_change_profile_picture'),
    path("subscription/", subscription, name="subscription"),
]
