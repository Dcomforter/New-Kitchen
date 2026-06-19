import json

from django.test import TestCase
from django.urls import reverse
from .models import Booking, Menu, Order
from django_countries.fields import Country

class BookingModelTest(TestCase):

    def setUp(self):
        self.booking = Booking.objects.create(
            first_name="Jenkins",
            last_name="User",
            sex="Male",
            email="jenkins.user@jenkins.com",
            phone_number="4025639856",
            guest_count=2,
            country="US",
            comments="Looking forward to it!",
        )

    def test_booking_creation(self):
        self.assertTrue(isinstance(self.booking, Booking))
        self.assertEqual(self.booking.__str__(), "Jenkins : User : Male : 2 :US")

    def test_booking_fields(self):
        self.assertEqual(self.booking.first_name, "Jenkins")
        self.assertEqual(self.booking.last_name, "User")
        self.assertEqual(self.booking.sex, "Male")
        self.assertEqual(self.booking.email, "jenkins.user@jenkins.com")
        self.assertEqual(self.booking.phone_number, "4025639856")
        self.assertEqual(self.booking.guest_count, 2)
        self.assertEqual(self.booking.country, Country("US"))
        self.assertEqual(self.booking.comments, "Looking forward to it!")
        self.assertIsNotNone(self.booking.date)
        self.assertIsNotNone(self.booking.time)

class MenuModelTest(TestCase):

    def setUp(self):
        self.menu_item = Menu.objects.create(
            food_name="Jollof Rice",
            cuisine="Western African",
            item_description="A classic Western African dish",
            price=12.99,
            prep_time=30,
            calories=850
        )

    def test_menu_creation(self):
        self.assertTrue(isinstance(self.menu_item, Menu))
        self.assertEqual(self.menu_item.__str__(), "Jollof Rice : Western African : 12.99 : 30 : 850")

    def test_menu_fields(self):
        self.assertEqual(self.menu_item.food_name, "Jollof Rice")
        self.assertEqual(self.menu_item.cuisine, "Western African")
        self.assertEqual(self.menu_item.item_description, "A classic Western African dish")
        self.assertEqual(self.menu_item.price, 12.99)
        self.assertEqual(self.menu_item.prep_time, 30)
        self.assertEqual(self.menu_item.calories, 850)


class MenuAPITest(TestCase):

    def setUp(self):
        self.menu_item = Menu.objects.create(
            food_name="Jollof Rice",
            cuisine="Western African",
            item_description="A classic Western African dish",
            price=12.99,
            prep_time=30,
            calories=850,
        )

    def test_menu_list_returns_items(self):
        response = self.client.get(reverse('api_menu_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['food_name'], "Jollof Rice")

    def test_menu_order_creates_fulfilled_order(self):
        response = self.client.post(
            reverse('api_menu_order', args=[self.menu_item.id]),
            data=json.dumps({
                'customer_name': 'Jane Doe',
                'customer_email': 'jane@example.com',
                'quantity': 2,
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.quantity, 2)
        self.assertTrue(order.fulfilled)


class CartAPITest(TestCase):

    def setUp(self):
        self.menu_item = Menu.objects.create(
            food_name="Jollof Rice",
            cuisine="Western African",
            item_description="A classic Western African dish",
            price=12.99,
            prep_time=30,
            calories=850,
        )

    def test_add_then_update_quantity(self):
        add_response = self.client.post(
            reverse('api_cart_add', args=[self.menu_item.id]),
            data=json.dumps({'quantity': 1}),
            content_type='application/json',
        )
        self.assertEqual(add_response.status_code, 201)

        patch_response = self.client.patch(
            reverse('api_cart_item', args=[self.menu_item.id]),
            data=json.dumps({'action': 'increase'}),
            content_type='application/json',
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.json()['quantity'], 2)
        self.assertEqual(patch_response.json()['subtotal'], '25.98')

    def test_checkout_creates_unfulfilled_order_and_clears_cart(self):
        self.client.post(
            reverse('api_cart_add', args=[self.menu_item.id]),
            data=json.dumps({'quantity': 3}),
            content_type='application/json',
        )

        checkout_response = self.client.post(
            reverse('api_cart_checkout'),
            data=json.dumps({
                'customer_name': 'Jane Doe',
                'customer_email': 'jane@example.com',
            }),
            content_type='application/json',
        )
        self.assertEqual(checkout_response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.quantity, 3)
        self.assertFalse(order.fulfilled)

        cart_response = self.client.get(reverse('api_cart_detail'))
        self.assertEqual(cart_response.json()['items'], [])
