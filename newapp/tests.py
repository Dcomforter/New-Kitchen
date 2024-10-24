from django.test import TestCase
from .models import Booking, Menu
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
