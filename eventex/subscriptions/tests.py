from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
    # def test_get(self):
    #     """Get /incricao/ must return code 200"""
    #     response = self.client.get('/inscricao/')
    #     self.assertEqual(200, response.status_code)
    #
    # def test_template(self):
    #     """Must use subscriptions/subscription_form.html"""
    #     response = self.client.get('/inscricao/')
    #     self.assertTemplateUsed(response, 'subscriptions/subscription_form.html')

    ##### Esta parte acima ele fez até passar os testes!...depois ele refatorou o código extraindo o "response" para o SetUp

    def setUp(self):
        self.resp = self.client.get('/inscricao/')


    def test_get(self):
        """Get /incricao/ must return code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """Html must contain CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    ## Neste teste estou amarrando meu Template HTML com o Django
    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """ Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))




