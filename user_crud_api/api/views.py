from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import (
    GetAllUserSerializer,
    GetSpecificUserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    DeleteUserSerializer,
)
from .pymongo import user_collection

# Create your views here.


class GetAllUserView(generics.ListAPIView):
    serializer_class = GetAllUserSerializer

    def get_queryset(self):
        serializer = self.serializer_class()
        queryset = serializer.get()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)


class GetSpecificUserView(generics.RetrieveAPIView):
    serializer_class = GetSpecificUserSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        serializer = self.serializer_class()
        queryset = serializer.get(user_id)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = serializer.data
            response["message"] = "User Registration: Successful"
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = serializer.data
            response["message"] = "User Updation: Successful"
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class DeleteUserView(generics.DestroyAPIView):
    serializer_class = DeleteUserSerializer

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = self.kwargs.get("user_id")
            scenario_archive_game = serializer.delete_game(user_id)

            response = scenario_archive_game
            response["message"] = "Scenario Game Deletion: Successful"
            response.pop("_id", None)
            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
