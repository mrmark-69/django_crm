import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from contracts.models import Contract
from products.models import Product


class ContractCreateViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.product_name = "service number unknown"
        self.contract_name = 'test_contract'
        self.product = Product.objects.create(name=self.product_name, price='333')
        Contract.objects.filter(name=self.contract_name).delete()

    def tearDown(self):
        self.product.delete()
        self.superuser.delete()
        super().tearDown()

    def test_create_contract(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse('contracts:add_contract'),
            {
                "name": self.contract_name,
                "product": self.product.pk,
                "date_signed": datetime.date,
                "start_date": datetime.date,
                "end_date": datetime.date,
                "amount": '335',
            }
        )
        self.assertRedirects(response, reverse("contracts:contracts_list"))
        self.assertTrue(
            Contract.objects.filter(name=self.contract_name).exists()
        )
        self.assertEqual(Contract.objects.count(), 1)

