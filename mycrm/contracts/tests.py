import datetime

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from contracts.models import Contract
from products.models import Product


class ContractListViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = User.objects.create_superuser(username='contract_username', password='password')

    @classmethod
    def tearDownClass(cls):
        cls.admin.delete()
        super().tearDownClass()

    def setUp(self) -> None:
        self.client.force_login(self.admin)

    def test_contracts_view(self):
        response = self.client.get(reverse("contracts:contracts_list"))
        self.assertContains(response, 'Контракты')

    def test_contracts_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('contracts:contracts_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, str(settings.LOGIN_URL) + "?next=/contracts/")
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ContractCreateViewTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='contracts_admin', password='password')
        self.product_name = "test_product"
        self.contract_name = 'test_contract'
        self.product = Product.objects.create(name=self.product_name, price='333')
        Contract.objects.filter(name=self.contract_name).delete()

    def tearDown(self):
        self.product.delete()
        self.superuser.delete()

    def test_create_contract(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse('contracts:add_contract'),
            {
                "name": self.contract_name,
                "product": self.product.pk,
                "date_signed": datetime.date.today(),
                "start_date": datetime.date.today(),
                "end_date": datetime.date.today(),
                "amount": '335',
            }
        )
        self.assertRedirects(response, reverse("contracts:contracts_list"))
        self.assertTrue(
            Contract.objects.filter(name=self.contract_name).exists()
        )
        self.assertEqual(Contract.objects.count(), 1)


class ContractDetailViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_superuser(username='contracts_test_user', password='password')
        permission = Permission.objects.get(codename='view_contract')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)
        self.product = Product.objects.create(name='test_product', price='666')
        self.contract = Contract.objects.create(
            name='Test contract # 1',
            product=self.product,
            date_signed=datetime.date.today(),
            start_date=datetime.date.today(),
            end_date=datetime.date.today(),
            amount='335',
        )

    def tearDown(self):
        self.contract.delete()
        self.product.delete()

    def test_contract_details(self):
        response = self.client.get(reverse('contracts:contracts_detail', args=[self.contract.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.contract.name, response.content.decode())
        self.assertIn(str(self.contract.product), response.content.decode())
        self.assertIn(self.contract.amount, response.content.decode())
        self.assertTrue(
            Contract.objects.filter(name='Test contract # 1').exists()
        )
        context_contract = response.context['contract']
        self.assertEqual(context_contract.pk, self.contract.pk)
