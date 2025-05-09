import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase


class EventTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
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

        # Remove the duplicate registration request

    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        url = "/events"
        data = {
            "volunteer": {
                "id": 1,
                "address": "123 yes way",
                "phone_number": "555-0125",
                "user": 10,
            },
            "title": "A fun Event",
            "location": {
                "id": 1,
                "city": "Nashville",
                "state": "Tn",
                "x_coordinate": "69.96",  # Sending as string
                "y_coordinate": "36.36",  # Sending as string
            },
            "time": "09:00:00",
            "date": "2025-05-25",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["title"], "A fun Event")
        self.assertEqual(json_response["time"], "09:00:00")
        self.assertEqual(json_response["date"], "2025-05-25")

        self.assertEqual(json_response["location"]["id"], 1)
        self.assertEqual(json_response["location"]["city"], "Nashville")
        self.assertEqual(json_response["location"]["state"], "Tn")

        # Updated to handle numeric values instead of strings
        self.assertEqual(float(json_response["location"]["x_coordinate"]), 69.96)
        self.assertEqual(float(json_response["location"]["y_coordinate"]), 36.36)

        self.assertEqual(json_response["volunteer"]["id"], 1)
        self.assertEqual(json_response["volunteer"]["address"], "123 yes way")
        self.assertEqual(json_response["volunteer"]["phone_number"], "555-0125")
        self.assertEqual(json_response["volunteer"]["user"], 1)

    def test_update_event(self):
        """
        Ensure we can update a product.
        """
        self.test_create_event()

        url = "/events/1"
        data = {
            "volunteer": {
                "id": 1,
                "address": "123 yes way",
                "phone_number": "555-0125",
                "user": 10,
            },
            "title": "A fun Event",
            "location": {
                "id": 1,
                "city": "Nashville",
                "state": "Tn",
                "x_coordinate": "69.96",  # Sending as string
                "y_coordinate": "36.36",  # Sending as string
            },
            "time": "09:00:00",
            "date": "2025-05-31",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(json_response["title"], "A fun Event")
        self.assertEqual(json_response["time"], "09:00:00")
        self.assertEqual(json_response["date"], "2025-05-31")
        self.assertEqual(json_response["location"]["id"], 1)
        self.assertEqual(json_response["location"]["city"], "Nashville")
        self.assertEqual(json_response["location"]["state"], "Tn")
        self.assertEqual(float(json_response["location"]["x_coordinate"]), 69.96)
        self.assertEqual(float(json_response["location"]["y_coordinate"]), 36.36)
        self.assertEqual(json_response["volunteer"]["id"], 1)
        self.assertEqual(json_response["volunteer"]["address"], "123 yes way")
        self.assertEqual(json_response["volunteer"]["phone_number"], "555-0125")
        self.assertEqual(json_response["volunteer"]["user"], 1)

    def test_get_all_events(self):
        """
        Ensure we can get a collection of products.
        """
        self.test_create_event()

        url = "/events"

        response = self.client.get(url, None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 1)

    def test_delete_event(self):
        """Ensure a event can be deleted"""
        self.test_create_event()
        url = "/events/1"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.delete(url, None, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
