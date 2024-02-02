from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from ads.models import Advertisement
from products.models import Product


class AdvertisementsListViewTest(TestCase):
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
        self.product = Product.objects.create(name='test_product', price='666')
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
        self.assertTrue(
            Advertisement.objects.filter(campaign_name='Advertisement # 1').exists()
        )
        context_advertisement = response.context['advertisement']
        self.assertEqual(context_advertisement.pk, self.advertisement.pk)


class AdvertisementCreateViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.superuser = User.objects.create_superuser(username='test_admin', password='password')
        cls.user_with_permission = User.objects.create_user(username='test_user', password='password')
        permission = Permission.objects.get(codename='add_advertisement')
        cls.user_with_permission.user_permissions.add(permission)
        cls.user_without_permission = User.objects.create_user(username='test_user_1', password='password')
        cls.url = reverse('ads:ads_new')
        cls.campaign_name = "Test Advertisement"
        Advertisement.objects.filter(campaign_name=cls.campaign_name).delete()

    @classmethod
    def tearDownClass(cls):
        cls.superuser.delete()
        cls.user_with_permission.delete()
        cls.user_without_permission.delete()

    def setUp(self):
        self.product = Product.objects.create(name='Test Product', price='333')

    def tearDown(self):
        self.product.delete()
        super().tearDown()

    def test_permission_required(self):
        self.client.force_login(self.user_without_permission)  # Пользователь без прав доступа.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)  # Проверяю, что в доступе отказано, если нет нужных прав.

    def test_get(self):
        self.client.force_login(self.user_with_permission)  # Пользователь с правом доступа.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Проверяю, что страница доступна при наличии прав
        self.assertTemplateUsed(response, 'ads/ads-create.html')  # Проверяю, что используется правильный шаблон

    def test_create_advertisement(self):
        self.client.force_login(self.superuser)  # Пользователь с правом доступа.
        response = self.client.post(
            self.url,
            {
                "campaign_name": self.campaign_name,
                "product": self.product.pk,
                "promotion_channel": "chanel_5",
                "advertisement_budget": "123",
            }
        )
        self.assertRedirects(response, reverse("ads:ads"))
        self.assertTrue(
            Advertisement.objects.filter(campaign_name=self.campaign_name).exists()
        )
        self.assertEqual(Advertisement.objects.count(), 1)  # Проверяю, что объект был создан
        advertisement = Advertisement.objects.first()
        self.assertEqual(advertisement.campaign_name,
                         'Test Advertisement')  # Проверяю, что заголовок соответствует введенным данным
        self.assertEqual(response.status_code,
                         302)  # Проверяю, что происходит редирект после успешного создания объекта
