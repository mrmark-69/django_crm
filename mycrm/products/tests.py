from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from products.models import Product


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.product_name = "service number unknown"
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse('products:add_product'),
            {
                "name": self.product_name,
                "description": 'newest product',
                "price": '150'
            }
        )
        self.assertRedirects(response, reverse("products:products_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_user = User.objects.create_superuser(username='admin', password='password')
        cls.product_name = "product unknown"
        cls.product = Product.objects.create(name=cls.product_name, price='999')

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.admin_user.delete()

    def test_get_product(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(
            reverse("products:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(
            reverse("products:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product_name)
