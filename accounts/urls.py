from django.urls import path

from .views import (
    UserListCreate,
    UserUpdate,
    ExtendedUserListCreate,
    ExtendedUserUpdate,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView


)


urlpatterns = [
    path('', UserListCreate.as_view()),
    path('<int:pk>/', UserUpdate.as_view()),
    path('extended/', ExtendedUserListCreate.as_view()),
    path('extended/<int:pk>/', ExtendedUserUpdate.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('password_reset/', PasswordResetRequestView.as_view()),
    path('password_reset_confirm/', PasswordResetConfirmView.as_view()),


    ]
