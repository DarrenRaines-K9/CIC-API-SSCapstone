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
from championsapi.models import Event, Volunteer


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    class Meta:
        model = Event
        fields = ("id", "volunteer", "title", "location", "time", "date")
        depth = 1


class Events(ViewSet):
    """Request handler for Events in the Champions API."""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """ "Haandle Post requests to create a new event."""

        new_event = Event()
        new_event.volunteer = request.data["volunteer"]
        new_event.title = request.data["title"]
        new_event.location = request.data["location"]
        new_event.time = request.data["time"]
        new_event.date = request.data["date"]

        volunteer = Volunteer.objects.get(pk=request.data["volunteer"])
        new_event.volunteer = volunteer
        volunteer.full_clean()
        volunteer.save()

        serializer = EventSerializer(
            new_event, many=False, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event"""

        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(
                event, many=False, context={"request": request}
            )
            response_data = serializer.data
            return Response(response_data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all events"""

        events = Event.objects.all()
        serializer = EventSerializer(events, many=True, context={"request": request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for an event"""

        event = Event.objects.get(pk=pk)
        event.volunteer = request.data["volunteer"]
        event.title = request.data["title"]
        event.location = request.data["location"]
        event.time = request.data["time"]
        event.date = request.data["date"]
        event.full_clean()
        event.save()
        volunteer = Volunteer.objects.get(user=request.auth.user)
        volunteer.full_clean()
        volunteer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for an event"""

        try:
            event = Event.objects.filter(pk=pk).first()
            event.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
