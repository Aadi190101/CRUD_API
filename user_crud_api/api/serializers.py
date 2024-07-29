from .pymongo import user_collection, id_collection
from rest_framework import serializers
from .utils import generate_random_string
import datetime


class GetAllUserSerializer(serializers.Serializer):
    def get(self):
        user_info = list(user_collection.find({}, {"_id": 0}))
        return user_info


class GetSpecificUserSerializer(serializers.Serializer):
    def get(self, user_id):
        if not user_collection.find_one({"user_id": user_id}, {"_id": 0}):
            raise serializers.ValidationError("No data found")
        user_info = list(user_collection.find({"user_id": user_id}, {"_id": 0}))
        return user_info


class CreateUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    mobile = serializers.IntegerField()
    email = serializers.EmailField(max_length=100)
    address = serializers.CharField(max_length=200)

    def validate(self, data):
        name = data.get("name")
        email = data.get("email")
        mobile = data.get("mobile")
        if not name.replace(" ", "").isalnum():
            raise serializers.ValidationError(
                "Full Name can only contain alphabets, digits, and spaces."
            )

        if user_collection.find_one({"email": email}):
            raise serializers.ValidationError(
                "Email address is already registered. Please provide another email address."
            )

        if len(str(mobile)) != 10:
            raise serializers.ValidationError(
                "Invalid mobile number. Enter a valid mobile number."
            )

        if user_collection.find_one({"mobile": mobile}):
            raise serializers.ValidationError(
                "Mobile number is already registered. Enter a valid mobile number."
            )
        return data

    def create(self, validated_data):
        user_id = generate_random_string("user_id", 10)

        current_time = datetime.datetime.now()

        user = {
            "user_id": user_id,
            "name": validated_data["name"],
            "mobile": validated_data["mobile"],
            "email": validated_data["email"],
            "address": validated_data["address"],
            "status": False,
            "created_at": current_time,
            "updated_at": current_time,
        }
        user_collection.insert_one(user)

        return user


class UpdateUserSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=100)
    mobile = serializers.IntegerField()
    email = serializers.EmailField(max_length=100)
    address = serializers.CharField(max_length=200)

    def validate(self, data):
        name = data.get("name")
        email = data.get("email")
        mobile = data.get("mobile")
        if not name.replace(" ", "").isalnum():
            raise serializers.ValidationError(
                "Full Name can only contain alphabets, digits, and spaces."
            )

        if user_collection.find_one({"email": email}):
            raise serializers.ValidationError(
                "Email address is already registered. Please provide another email address."
            )

        if len(str(mobile)) != 10:
            raise serializers.ValidationError(
                "Invalid mobile number. Enter a valid mobile number."
            )

        if user_collection.find_one({"mobile_number": mobile}):
            raise serializers.ValidationError(
                "Mobile number is already registered. Enter a valid mobile number."
            )
        return data

    def create(self, validated_data):
        # if not user_collection.find_one({"user_id": validated_data["user_id"]}):
        #     raise serializers.ValidationError(f"No user found with user_id:{validated_data["user_id"]}")

        user = {
            "user_id": validated_data["user_id"],
            "name": validated_data["name"],
            "mobile": validated_data["mobile"],
            "email": validated_data["email"],
            "address": validated_data["address"],
            "status": False,
            "updated_at": datetime.datetime.now(),
        }
        user_collection.update_one(
            {"user_id": validated_data["user_id"]},
            {"$set": user},
        )

        return user


class DeleteUserSerializer(serializers.Serializer):
    def delete_game(self, user_id):
        user_collection.delete_one({"user_id": user_id})
        id_collection.delete_one(({"id": user_id}))
        return {"deleted": user_id}
