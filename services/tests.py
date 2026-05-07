from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from services.models import Category, Service


class ServiceViewsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Consultoria')
        self.service = Service.objects.create(
            name='BPO Financeiro',
            description='Servico de terceirizacao financeira.',
            category=self.category,
            billing_model='Mensal',
            price=1500.00,
        )

    def test_services_page_lists_existing_services(self):
        response = self.client.get(reverse('services'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BPO Financeiro')

    def test_services_page_filters_by_name(self):
        Service.objects.create(
            name='Gestao de Folha',
            description='Servico de gestao de folha.',
            category=self.category,
            billing_model='Mensal',
            price=900.00,
        )

        response = self.client.get(reverse('services'), {'search': 'BPO'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BPO Financeiro')
        self.assertNotContains(response, 'Gestao de Folha')

    def test_new_service_redirects_anonymous_user_to_login(self):
        response = self.client.get(reverse('new_service'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])

    def test_authenticated_user_can_open_new_service_form(self):
        User.objects.create_user(username='admin', password='senha-forte')
        self.client.login(username='admin', password='senha-forte')

        response = self.client.get(reverse('new_service'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Criar Serviço')

