from django.urls import path

from .views import (
    UserListCreate,
    UserUpdate,
    GroupList,
    PermissionList,
    ExtendedUserListCreate,
    ExtendedUserUpdate


)


urlpatterns = [
    path('', UserListCreate.as_view()),
    path('<int:pk>/', UserUpdate.as_view()),
    path('group/', GroupList.as_view()),
    path('permission/', PermissionList.as_view()),
    path('extended/', ExtendedUserListCreate.as_view()),
    path('extended/<int:pk>/', ExtendedUserUpdate.as_view()),
    #path('change_password/', ChangePassword.as_view()),
    #path('password_reset/', PasswordReset.as_view()),
    #path('password_reset_confirm/', PasswordResetConfirm.as_view()),
    #path('token/', CustomTokenObtainPairView.as_view()),

    ]
