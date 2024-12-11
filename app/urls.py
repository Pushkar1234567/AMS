from django.contrib import admin
from django.urls import path
from .views import Register,CustomTokenObtainPairView,UserDetailView, RosterView, ShiftView, AttendanceView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', Register.as_view(), name = 'register_user'),
    # path('add/staff/', StaffCreationView.as_view(), name = 'register_user'),
    path('users/', UserDetailView.as_view(), name='Users'),
    path('roster/', RosterView.as_view(), name='roster'),
    path('shifts/', ShiftView.as_view(), name='shifts'),
    path('attendance/', AttendanceView.as_view(), name='attendance'),

    # JWT endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)