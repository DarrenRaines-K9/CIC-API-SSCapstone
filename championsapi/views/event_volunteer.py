from rest_framework.decorators import action
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from championsapi.models import Event, Volunteer, EventVolunteer


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    class Meta:
        model = Event
        fields = (
            "id",
            "volunteers",
            "volunteer",
            "title",
            "location",
            "time",
            "date",
        )
        depth = 0


class EventVolunteerSerializer(serializers.ModelSerializer):
    """JSON serializer for event volunteers"""

    class Meta:
        model = EventVolunteer
        fields = ("id", "event", "volunteer")
        depth = 1


class EventVolunteers(ViewSet):
    """Request handler for Event Volunteers in the Champions API."""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """ "Handle Post requests to create a new event volunteer."""

        try:
            event_volunteer = EventVolunteer()
            event = Event.objects.get(pk=request.data["event"])
            volunteer = Volunteer.objects.get(user=request.auth.user)
            event_volunteer.event = event
            event_volunteer.volunteer = volunteer
            event_volunteer.full_clean()
            event_volunteer.save()
            serializer = EventVolunteerSerializer(
                event_volunteer, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event volunteer"""

        try:
            event_volunteer = EventVolunteer.objects.get(pk=pk)
            serializer = EventSerializer(
                event_volunteer, many=False, context={"request": request}
            )
            response_data = serializer.data
        except EventVolunteer.DoesNotExist as ex:
            return Response({"message": str(ex)}, status=status.HTTP_404_NOT_FOUND)

        return Response(response_data)

    def list(self, request):
        """Handle GET requests to event volunteers resource"""

        events = Event.objects.all()

        serializer = EventSerializer(events, many=True, context={"request": request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for an event volunteer"""

        try:
            event_volunteer = EventVolunteer.objects.get(pk=pk)
            event_volunteer.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except EventVolunteer.DoesNotExist as ex:
            return Response({"message": str(ex)}, status=status.HTTP_404_NOT_FOUND)
