from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from ads.models import Advertisement
from leads.models import Lead
from products.models import Product


class LeadsListViewTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(username='lead_admin', password='password')

    def tearDown(self):
        self.admin.delete()

    def test_leads_view(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('leads:leads'))
        self.assertContains(response, 'Лиды')

    def test_leads_view_not_authenticated(self):
        response = self.client.get(reverse('leads:leads'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, str(settings.LOGIN_URL) + "?next=/leads/")
        self.assertIn(str(settings.LOGIN_URL), response.url)


class LeadDetailsViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='leads_user', password='password')
        permission = Permission.objects.get(codename='view_lead')
        self.user.user_permissions.add(permission)
        self.client.force_login(self.user)
        self.product = Product.objects.create(name='test_product', price='666')
        self.campaign = Advertisement.objects.create(
            campaign_name='Advertisement # 1',
            product=self.product,
            advertisement_budget='155',
        )
        self.lead = Lead.objects.create(
            first_name='First_test',
            last_name='Last_test',
            phone='+12343529735',
            email='fl@mail.com',
            campaign=self.campaign
        )

    def tearDown(self):
        self.user.delete()
        self.campaign.delete()
        self.lead.delete()
        self.product.delete()

    def test_lead_details(self):
        response = self.client.get(reverse('leads:leads_detail', args=[self.lead.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.lead.first_name, response.content.decode())
        self.assertIn(str(self.lead.last_name), response.content.decode())
        self.assertIn(self.lead.phone, response.content.decode())
        self.assertTrue(
            Lead.objects.filter(first_name='First_test').exists()
        )
        context_lead = response.context['lead']
        self.assertEqual(context_lead.pk, self.lead.pk)


class LeadCreateViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_with_permission = User.objects.create_user(username='test_user',
                                                            password='password')  # Пользователь с доступом
        permission = Permission.objects.get(codename='add_lead')
        permission_2 = Permission.objects.get(codename='view_lead')
        cls.user_with_permission.user_permissions.add(permission)
        cls.user_with_permission.user_permissions.add(permission_2)
        cls.user_without_permission = User.objects.create_user(username='test_user_1',
                                                               password='password')  # Пользователь без доступа
        cls.url = reverse('leads:add_lead')
        cls.lead_name = "Firs_test"
        Lead.objects.filter(first_name=cls.lead_name).delete()

    @classmethod
    def tearDownClass(cls):
        cls.user_with_permission.delete()
        cls.user_without_permission.delete()
        super().tearDownClass()

    def setUp(self):
        self.product = Product.objects.create(name='Test Product', price='333')
        self.campaign = Advertisement.objects.create(
            campaign_name='Advertisement # 1',
            product=self.product,
            advertisement_budget='155',
        )

    def tearDown(self):
        self.product.delete()
        self.campaign.delete()

    def test_permission_required(self):
        self.client.force_login(self.user_without_permission)  # Пользователь без прав доступа.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)  # Проверяю, что в доступе отказано, если нет нужных прав.

    def test_get(self):
        self.client.force_login(self.user_with_permission)  # Пользователь с правом доступа.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Проверяю, что страница доступна при наличии прав
        self.assertTemplateUsed(response, 'leads/leads-create.html')  # Проверяю, что используется правильный шаблон

    def test_create_lead(self):
        self.client.force_login(self.user_with_permission)  # Пользователь с правом создавать лида.
        response = self.client.post(
            self.url,
            {
                "first_name": self.lead_name,
                "last_name": 'Last',
                "phone": "+12546753287",
                "email": "123@mail.com",
                "campaign": self.campaign.pk,
            }
        )
        self.assertRedirects(response, reverse("leads:leads"))
        self.assertTrue(
            Lead.objects.filter(first_name=self.lead_name).exists()
        )
        self.assertEqual(Lead.objects.count(), 1)  # Проверяю, что объект был создан
        lead = Lead.objects.first()
        self.assertEqual(lead.phone,
                         "+12546753287")  # Проверяю, что телефон соответствует введенным данным
        self.assertEqual(response.status_code,
                         302)  # Проверяю, что происходит редирект после успешного создания объекта
