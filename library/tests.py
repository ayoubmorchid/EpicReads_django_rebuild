from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Book, Category


class PublicPagesTests(TestCase):
    def test_public_pages_load_successfully(self):
        client = Client()
        for url_name in ["home", "book_list", "about", "contact", "login", "register"]:
            response = client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200, url_name)


class BookFlowTests(TestCase):
    def setUp(self):
        self.category, _ = Category.objects.get_or_create(name="Test Technology")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            category=self.category,
            description="A small test book description.",
            available=True,
        )
        self.user = User.objects.create_user(username="reader", password="secret123")

    def test_book_detail_loads(self):
        response = self.client.get(reverse("book_detail", args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_authenticated_user_can_add_book_to_cart(self):
        self.client.login(username="reader", password="secret123")
        response = self.client.get(f"{reverse('checkout')}?book={self.book.pk}")
        self.assertRedirects(response, reverse("checkout"))
        self.assertEqual(self.client.session["cart"], {str(self.book.pk): 1})

    def test_authenticated_user_can_toggle_favorite(self):
        self.client.login(username="reader", password="secret123")
        response = self.client.post(
            reverse("favorite_toggle", args=[self.book.pk]),
            {"next": reverse("book_list")},
        )
        self.assertRedirects(response, reverse("book_list"))
        self.assertEqual(self.client.session["favorites"], [self.book.pk])
