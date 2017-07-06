from django.core import mail
from django.test import TestCase


class SubscribeValid(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='12345678901',
                    email='henrique@bastos.net', phone='21-99618-6180')

        ''' Após a criação deste "test_mail_subscribe", não precisamos mais do "self.resp", pois vamos refatorar
         só para o e-mail como logo abaixo'''
        # self.resp = self.client.post('/inscricao/', data)
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]



    ## Aqui estamos escrevendo um teste para a formatação dos e-mails, no caso o "Subject"
    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    ## Aqui estamos escrevendo um teste para a formatação dos e-mails, no caso o "Remetente"
    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    ## Aqui estamos escrevendo um teste para a formatação dos e-mails, no caso o "Destinatário"
    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'henrique@bastos.net']

        self.assertEqual(expect, self.email.to)

    ## Aqui estamos escrevendo um teste para a formatação dos e-mails, no caso o CORPO DO E-MAIL"
    def test_subscription_email_body(self):
        contents = [
            'Henrique Bastos',
            '12345678901',
            'henrique@bastos.net',
            '21-99618-6180',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

