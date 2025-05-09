import json
from rest_framework import status
from rest_framework.test import APITestCase


class InventoryTests(APITestCase):
    def setUp(self) -> None:
        """
        Register a volunteer and get auth token
        """
        url = "/register"
        data = {
            "username": "mike",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "123 yes way",
            "phone_number": "555-0125",
            "first_name": "Mike",
            "last_name": "Brownlee",
        }
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_inventory_item(self):
        """
        Ensure we can create a new inventory item (Paper Plates).
        """
        url = "/inventory"
        data = {
            "volunteer": {
                "id": 1,
                "address": "123 yes way",
                "phone_number": "555-0125",
                "user": 1,
            },
            "name": "Paper Plates",
            "quantity": 100,
            "description": "Biodegradable plates for events and food distribution",
            "cost": "4.50",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Paper Plates")
        self.assertEqual(json_response["quantity"], 100)
        self.assertEqual(
            json_response["description"],
            "Biodegradable plates for events and food distribution",
        )
        self.assertEqual(float(json_response["cost"]), 4.50)
        self.assertEqual(json_response["volunteer"]["id"], 1)

    def test_update_inventory_item(self):
        """
        Ensure we can update the Paper Plates inventory item.
        """
        self.test_create_inventory_item()

        url = "/inventory/1"
        updated_data = {
            "volunteer": {
                "id": 1,
                "address": "123 yes way",
                "phone_number": "555-0125",
                "user": 1,
            },
            "name": "Paper Plates - Large Pack",
            "quantity": 120,
            "description": "Updated: More plates per pack",
            "cost": "5.25",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get and verify update
        response = self.client.get(url, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(json_response["name"], "Paper Plates - Large Pack")
        self.assertEqual(json_response["quantity"], 120)
        self.assertEqual(json_response["description"], "Updated: More plates per pack")
        self.assertEqual(float(json_response["cost"]), 5.25)

    def test_get_all_inventory_items(self):
        """
        Ensure we can retrieve all inventory items.
        """
        self.test_create_inventory_item()

        url = "/inventory"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get(url, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(json_response), 1)

    def test_delete_inventory_item(self):
        """
        Ensure we can delete the Paper Plates inventory item.
        """
        self.test_create_inventory_item()

        url = "/inventory/1"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
