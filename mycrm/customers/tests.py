import datetime

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from ads.models import Advertisement
from contracts.models import Contract
from customers.models import Customer
from leads.models import Lead
from products.models import Product


class CustomerListViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='customer_test_user', password='password')
        permission = Permission.objects.get(codename='view_customer')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_customers_view(self):
        response = self.client.get(reverse("customers:customers_list"))
        self.assertContains(response, 'Активные клиенты')

    def test_customers_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('customers:customers_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, str(settings.LOGIN_URL) + "?next=/customers/")
        self.assertIn(str(settings.LOGIN_URL), response.url)


class CustomerCreateViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.superuser = User.objects.create_superuser(username='customer_admin', password='password')
        self.product = Product.objects.create(name='test_product', price='666')
        self.campaign = Advertisement.objects.create(
            campaign_name='Advertisement # 1',
            product=self.product,
            advertisement_budget='155',
        )
        self.lead = Lead.objects.create(
            first_name='First',
            last_name='Last',
            phone ='+13298237382',
            email ='f@mail.com',
            campaign =self.campaign
                                        )
        self.contract = Contract.objects.create(
            name='Test contract # 1',
            product=self.product,
            date_signed=datetime.date.today(),
            start_date=datetime.date.today(),
            end_date=datetime.date.today(),
            amount='335',
        )
        Customer.objects.filter(lead=self.lead.pk).delete()

    def tearDown(self):
        self.product.delete()
        self.campaign.delete()
        self.lead.delete()
        self.contract.delete()
        self.superuser.delete()
        super().tearDown()

    def test_create_contract(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse('customers:add_customers'),
            {
                "lead": self.lead.pk,
                "contract": self.contract.pk,
            }
        )
        self.assertRedirects(response, reverse("customers:customers_list"))
        self.assertTrue(
            Customer.objects.filter(lead=self.lead).exists()
        )
        self.assertEqual(Customer.objects.count(), 1)


class CustomerDetailsViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_superuser(username='customer_user', password='password')


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.product = Product.objects.create(name='test_product', price='666')
        self.campaign = Advertisement.objects.create(
            campaign_name='Advertisement # 1',
            product=self.product,
            advertisement_budget='155',
        )
        self.lead = Lead.objects.create(
            first_name='First',
            last_name='Last',
            phone='+13298237382',
            email='f@mail.com',
            campaign=self.campaign
        )
        self.contract = Contract.objects.create(
            name='Test contract # 1',
            product=self.product,
            date_signed=datetime.date.today(),
            start_date=datetime.date.today(),
            end_date=datetime.date.today(),
            amount='335',
        )
        self.customer = Customer.objects.create(lead=self.lead, contract=self.contract)

    def tearDown(self):
        self.contract.delete()
        self.customer.delete()
        self.lead.delete()
        self.campaign.delete()
        self.product.delete()
        super().tearDown()

    def test_customer_details(self):
        response = self.client.get(reverse('customers:customers_detail', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.customer.lead.first_name, response.content.decode())
        self.assertIn(self.customer.contract.name, response.content.decode())
        self.assertTrue(
            Customer.objects.filter(lead=self.lead).exists()
        )
        context_customer = response.context['customer']
        self.assertEqual(context_customer.pk, self.customer.pk)
