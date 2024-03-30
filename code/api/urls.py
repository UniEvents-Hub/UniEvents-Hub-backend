from django.urls import path
from .views import UserProfileRetrieveUpdateAPIView, UpdateUserProfileAPIView

urlpatterns = [
    path('updateuserprofile/<int:pk>/', UpdateUserProfileAPIView.as_view(), name='user-profile-update'),
    path('userprofile/<int:pk>/', UserProfileRetrieveUpdateAPIView.as_view(), name='user-profile-retrieve'),
]
