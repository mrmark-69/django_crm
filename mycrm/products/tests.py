from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from products.models import Product


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.product_name = "service number unknown"
        Product.objects.filter(name=self.product_name).delete()

    def tearDown(self):
        self.superuser.delete()
        super().tearDown()

    def test_create_product(self):
        self.client.login(username='admin', password='password')
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
        self.assertEqual(Product.objects.count(), 1)


class ProductDetailViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = User.objects.create_superuser(username='admin', password='password')
        cls.product_name = "product noname"
        cls.product = Product.objects.create(name=cls.product_name, price='999')

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.admin.delete()
        super().tearDownClass()

    def setUp(self) -> None:
        self.client.force_login(self.admin)

    def test_get_product(self):
        response = self.client.get(
            reverse("products:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("products:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product_name)

    def test_get_product_and_check_template_used(self):
        response = self.client.get(
            reverse("products:product_details", kwargs={"pk": self.product.pk})
        )
        self.assertTemplateUsed(response, "products/products-detail.html")

    def test_get_product_with_invalid_pk(self):
        response = self.client.get(
            reverse("products:product_details", kwargs={"pk": 0})
        )
        self.assertEqual(response.status_code, 404)


class ProductListViewTestCase(TestCase):

    def test_products(self):
        response = self.client.get(reverse('products:products_list'))
        self.assertQuerysetEqual(
            qs=Product.objects.all(),
            values=(p.pk for p in response.context['products']),
            transform=lambda p: p.pk,
            ordered=False
        )
        self.assertTemplateUsed(response, 'products/products-list.html')
