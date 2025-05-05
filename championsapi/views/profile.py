"""View module for handling requests about customer profiles"""

from django.http import HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from championsapi.models import Volunteer
from django.contrib.auth.models import User


class Profile(ViewSet):
    """Request handlers for user profile info in the Champions in Christ Platform"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """
        @api {GET} /profile GET user profile info
        @apiName GetProfile
        @apiGroup UserProfile

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiSuccess (200) {Number} id Profile id
        @apiSuccess (200) {String} url URI of volunteer profile
        @apiSuccess (200) {Object} user Related user object
        @apiSuccess (200) {String} user.first_name Volunteer first name
        @apiSuccess (200) {String} user.last_name Volunteer last name
        @apiSuccess (200) {String} user.email Volunteer email
        @apiSuccess (200) {String} phone_number Volunteer phone number
        @apiSuccess (200) {String} address Volunteer address

        @apiSuccessExample {json} Success
            HTTP/1.1 200 OK
            {
                "id": 7,
                "url": "http://localhost:8000/volunteers/7",
                "user": {
                    "first_name": "Brenda",
                    "last_name": "Long",
                    "email": "brenda@brendalong.com"
                },
                "phone_number": "555-1212",
                "address": "100 Indefatiguable Way"
            }
        """
        try:
            current_user = Volunteer.objects.get(user=request.auth.user)
            serializer = ProfileSerializer(
                current_user, many=False, context={"request": request}
            )

            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(
                {"message": "Profile not found for current user"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        @api {PUT} /profile UPDATE user profile info
        @apiName UpdateProfile
        @apiGroup UserProfile

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {String} first_name User first name
        @apiParam {String} last_name User last name
        @apiParam {String} email User email
        @apiParam {String} phone_number User phone number
        @apiParam {String} address User address

        @apiParamExample {json} Input
            {
                "first_name": "Brenda",
                "last_name": "Long",
                "email": "brenda@brendalong.com",
                "phone_number": "555-1212",
                "address": "100 Indefatiguable Way"
            }

        @apiSuccess (200) {Object} profile Updated profile information

        @apiSuccessExample {json} Success
            HTTP/1.1 200 OK
            {
                "id": 7,
                "user": {
                    "first_name": "Brenda",
                    "last_name": "Long",
                    "email": "brenda@brendalong.com"
                },
                "phone_number": "555-1212",
                "address": "100 Indefatiguable Way",
                "is_admin": false
            }
        """
        try:
            # Get the current volunteer
            volunteer = Volunteer.objects.get(user=request.auth.user)

            # Update User model fields
            user = request.auth.user
            user.first_name = request.data.get("first_name", user.first_name)
            user.last_name = request.data.get("last_name", user.last_name)
            user.email = request.data.get("email", user.email)
            user.save()

            # Update Volunteer model fields
            volunteer.phone_number = request.data.get(
                "phone_number", volunteer.phone_number
            )
            volunteer.address = request.data.get("address", volunteer.address)
            volunteer.save()

            # Return the updated profile
            serializer = ProfileSerializer(user, context={"request": request})
            serializer = ProfileSerializer(volunteer, context={"request": request})
            return Response(serializer.data)

        except ObjectDoesNotExist:
            return Response(
                {"message": "Profile not found for current user"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            return HttpResponseServerError(ex)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user profiles"""

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
        depth = 1


class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for user profiles"""

    # user = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    user = UserSerializer(many=False)

    class Meta:
        model = Volunteer
        fields = ("id", "user", "phone_number", "address", "is_admin")
        depth = 2

    # def get_user(self, obj):
    #     return {
    #         "first_name": obj.user.first_name,
    #         "last_name": obj.user.last_name,
    #         "email": obj.user.email,
    #     }

    def get_is_admin(self, obj):
        if obj.user.is_staff:
            return True
        else:
            return False
