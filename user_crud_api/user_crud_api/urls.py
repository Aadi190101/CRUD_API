from django.contrib import admin
from django.urls import path, include
from api.views import *

urlpatterns = [
    path("get/all/", GetAllUserView.as_view(), name="get-user"),
    path(
        "get/specific/<slug:user_id>/",
        GetSpecificUserView.as_view(),
        name="get-specific-user",
    ),
    path("create/", CreateUserView.as_view(), name="create-user"),
    path("update/", UpdateUserView.as_view(), name="update-specific-user"),
    path(
        "delete/<slug:user_id>", DeleteUserView.as_view(), name="delete-specific-user"
    ),
]
