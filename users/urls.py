from django.urls import path
from .views import SignUpView, UserDetailsView, UpdateUserView, DeleteUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('details/', UserDetailsView.as_view(), name='user-details'),
    path('update/', UpdateUserView.as_view(), name='user-update'),
    path('delete/', DeleteUserView.as_view(), name='user-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
