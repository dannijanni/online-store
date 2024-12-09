from django.test import TestCase
from django.urls import reverse
from products.models import Product
from order_manager.models import Cart, Order
from django.contrib.auth.models import User

class IntegrationTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        # Create test products
        self.product1 = Product.objects.create(name="Product 1", price=50.00, stock=20)
        self.product2 = Product.objects.create(name="Product 2", price=30.00, stock=15)

        # Define URLs
        self.add_to_cart_url = reverse("add_to_cart", args=[self.product1.id])
        self.cart_url = reverse("cart")
        self.checkout_url = reverse("checkout")

    def test_cart_to_order_flow(self):
        # Add products to the cart
        response = self.client.post(self.add_to_cart_url, {"quantity": 2})
        self.assertEqual(response.status_code, 302)  # Redirect to cart page

        # Verify cart content
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.products.count(), 1)
        self.assertEqual(cart.total, 100.00)

        # Proceed to checkout
        response = self.client.post(self.checkout_url, {"address": "123 Test Street", "payment_method": "card"})
        self.assertEqual(response.status_code, 302)  # Redirect to order confirmation page

        # Verify order creation
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total, 100.00)
        self.assertEqual(order.products.count(), 1)
        self.assertEqual(order.address, "123 Test Street")

        # Verify stock reduction
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 18)  # Original stock (20) - purchased quantity (2)

    def test_insufficient_stock_handling(self):
        # Try adding more products than available stock
        response = self.client.post(reverse("add_to_cart", args=[self.product1.id]), {"quantity": 25})
        self.assertEqual(response.status_code, 400)  # Bad request due to insufficient stock

        # Verify no product was added to the cart
        cart = Cart.objects.filter(user=self.user).first()
        self.assertIsNone(cart)  # Cart shouldn't exist yet
