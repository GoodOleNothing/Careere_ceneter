from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from .models import NetworkNode
from rest_framework.test import APITestCase

User = get_user_model()


class NetworkNodeModelTest(TestCase):

    def setUp(self):
        self.factory = NetworkNode.objects.create(
            name="Завод A",
            email="a@factory.com",
            country="RU",
            city="Moscow",
            street="Lenina",
            house_number="1",
            supplier=None
        )

        self.retail = NetworkNode.objects.create(
            name="Сеть B",
            email="b@retail.com",
            country="RU",
            city="Moscow",
            street="Tverskaya",
            house_number="10",
            supplier=self.factory
        )

        self.individual = NetworkNode.objects.create(
            name="ИП C",
            email="c@ip.com",
            country="RU",
            city="Kazan",
            street="Central",
            house_number="5",
            supplier=self.retail
        )

    def test_levels(self):
        self.assertEqual(self.factory.level, 0)
        self.assertEqual(self.retail.level, 1)
        self.assertEqual(self.individual.level, 2)

    def test_cannot_create_level_3(self):
        with self.assertRaises(ValidationError):
            node = NetworkNode(
                name="D",
                email="d@ip.com",
                country="RU",
                city="Samara",
                street="Sovetskaya",
                house_number="7",
                supplier=self.individual
            )
            node.full_clean()

    def test_cannot_update_above_level_limit(self):
        self.individual.supplier = self.individual

        with self.assertRaises(ValidationError):
            node = NetworkNode(
                name="D",
                email="d@ip.com",
                country="RU",
                city="Samara",
                street="Sovetskaya",
                house_number="7",
                supplier=self.individual  # уровень
            )
            node.full_clean()


class NetworkNodeAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@example.com",
            password="admin123",
            phone="89999999",
            is_active=True,
            is_staff=True
        )
        self.client.force_authenticate(user=self.user)

        self.non_staff_user = User.objects.create_user(
            id=1,
            email="user@example.com",
            password="user123",
            phone="89999998",
            is_active=True,
            is_staff=False
        )

        self.factory = NetworkNode.objects.create(
            name="Завод A",
            email="a@factory.com",
            country="RU",
            city="Moscow",
            street="Lenina",
            house_number="1"
        )

        self.url = reverse("network:nodes-list")

    def test_create_node(self):
        response = self.client.post(self.url, {
            "name": "Сеть B",
            "email": "b@retail.com",
            "country": "RU",
            "city": "Moscow",
            "street": "Tverskaya",
            "house_number": "10",
            "supplier": self.factory.id,
            "debt": "1000.00"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_update_debt(self):
        node = NetworkNode.objects.create(
            name="Сеть B",
            email="b@retail.com",
            country="RU",
            city="Moscow",
            street="Tverskaya",
            house_number="10",
            supplier=self.factory,
            debt="1500.00"
        )
        response = self.client.patch(reverse("network:nodes-detail", args=[node.id]), {
            "debt": "0.00"
        })
        node.refresh_from_db()
        self.assertEqual(node.debt, 1500.00)

    def test_filter_by_country(self):
        response = self.client.get(self.url + "?country=RU")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_non_staff_user_cannot_access_api(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.non_staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
