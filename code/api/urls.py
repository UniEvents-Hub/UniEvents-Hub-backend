from django.urls import path
from .views import UserProfileRetrieveUpdateAPIView, UpdateUserProfileAPIView,UserExistsAPIView

urlpatterns = [
    path('updateuserprofile/<int:pk>/', UpdateUserProfileAPIView.as_view(), name='user-profile-update'),
    path('userprofile/<int:pk>/', UserProfileRetrieveUpdateAPIView.as_view(), name='user-profile-retrieve'),
    path('userexists/<str:username>/', UserExistsAPIView.as_view(), name='user-profile-exists'),
]
