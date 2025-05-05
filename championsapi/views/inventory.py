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
from championsapi.models import Inventory, Volunteer


class InventorySerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    class Meta:
        model = Inventory
        fields = ("id", "volunteer", "name", "quantity", "description", "cost")
        depth = 1


class InventoryViewset(ViewSet):
    """Request handler for Inventory in the Champions API."""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """ "Handle Post requests to create a new event."""

        new_inventory = Inventory()
        volunteer = Volunteer.objects.get(user=request.auth.user)
        new_inventory.name = request.data["name"]
        new_inventory.quantity = request.data["quantity"]
        new_inventory.description = request.data["description"]
        new_inventory.cost = request.data["cost"]
        new_inventory.volunteer = volunteer
        new_inventory.full_clean()
        new_inventory.save()

        serializer = InventorySerializer(
            new_inventory, many=False, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event"""

        try:
            inventory = Inventory.objects.get(pk=pk)
            serializer = InventorySerializer(
                inventory, many=False, context={"request": request}
            )
            response_data = serializer.data
            return Response(response_data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all events"""

        inventory = Inventory.objects.all()
        serializer = InventorySerializer(
            inventory, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for an event"""

        inventory = Inventory.objects.get(pk=pk)
        inventory.name = request.data["name"]
        inventory.quantity = request.data["quantity"]
        inventory.description = request.data["description"]
        inventory.cost = request.data["cost"]
        inventory.full_clean()
        inventory.save()
        volunteer = Volunteer.objects.get(user=request.auth.user)
        volunteer.full_clean()
        volunteer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for an event"""

        try:
            inventory = Inventory.objects.filter(pk=pk).first()
            inventory.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Inventory.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
