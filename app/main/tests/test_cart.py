from django.test import TestCase
from django.urls import reverse
from products.models import Product
from order_manager.models import Cart

class CartTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100.00, stock=10)
        self.cart_url = reverse("cart")
        self.add_to_cart_url = reverse("add_to_cart", args=[self.product.id])
        self.remove_from_cart_url = reverse("remove_from_cart", args=[self.product.id])

    def test_add_to_cart(self):
        response = self.client.post(self.add_to_cart_url, {"quantity": 1})
        self.assertEqual(response.status_code, 302)  # Assuming redirect to the cart page
        cart = Cart.objects.first()
        self.assertIsNotNone(cart)
        self.assertEqual(cart.products.count(), 1)

    def test_remove_from_cart(self):
        self.client.post(self.add_to_cart_url, {"quantity": 1})
        response = self.client.post(self.remove_from_cart_url)
        self.assertEqual(response.status_code, 302)  # Assuming redirect to the cart page
        cart = Cart.objects.first()
        self.assertEqual(cart.products.count(), 0)

    def test_cart_total(self):
        self.client.post(self.add_to_cart_url, {"quantity": 2})
        cart = Cart.objects.first()
        self.assertEqual(cart.total, 200.00)  # 2 * product price
