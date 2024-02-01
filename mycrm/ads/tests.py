from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from ads.models import Advertisement
from products.models import Product


class AdvertisementsListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = User.objects.create_superuser(username='admin', password='password')

    @classmethod
    def tearDownClass(cls):
        cls.admin.delete()
        super().tearDownClass()

    def setUp(self) -> None:
        self.client.force_login(self.admin)

    def test_ads_view(self):
        response = self.client.get(reverse('ads:ads'))
        self.assertContains(response, 'Рекламные компании')

    def test_ads_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('ads:ads'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, str(settings.LOGIN_URL) + "?next=/ads/")
        self.assertIn(str(settings.LOGIN_URL), response.url)


class AdvertisementDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user', password='password')
        permission = Permission.objects.get(codename='view_advertisement')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.product = Product.objects.create(name='Product', price='666')
        self.advertisement = Advertisement.objects.create(
            campaign_name='Advertisement # 1',
            product=self.product,
            advertisement_budget='155',
        )

    def tearDown(self):
        self.advertisement.delete()
        self.product.delete()
        super().tearDown()

    def test_advertisement_details(self):
        response = self.client.get(reverse('ads:ads_details', args=[self.advertisement.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.advertisement.campaign_name, response.content.decode())
        self.assertIn(str(self.advertisement.product), response.content.decode())
        self.assertIn(self.advertisement.advertisement_budget, response.content.decode())

        context_advertisement = response.context['advertisement']
        self.assertEqual(context_advertisement.pk, self.advertisement.pk)
