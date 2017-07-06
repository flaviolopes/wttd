from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTEst(TestCase):
    def setUp(self):
        self.form = SubscriptionForm()

    def test_form_has_fields(self):
        # """ Form must have 4 fields"""
        # form = self.resp.context['form']
        # self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(self.form.fields))

