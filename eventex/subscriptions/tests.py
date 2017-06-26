from django.core import mail
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

## Esta é a que ele criou para o "post" de informações quando o usuário preenche o formulário
# class SubscribePostTest(TestCase):
#     def test_post(self):
#         """Valid POST should redirect to /inscricao/"""
#
#         ## esta variável "data" está simulando o recebimento das informações digitadas em nosso formulário
#         data = dict(name='Henrique Bastos', cpf='12345678901',
#                     email='henrique@bastos.net', phone='21-99618-6180')
#
#         response = self.client.post('/inscricao/', data)
#
#         ## o código "302" é o código de redirecionamento de paginas web. Pois nesse caso, após o "post" queremos
#         ## redirecionar o usuário de volta para a página de inscrição
#         self.assertEqual(302, response.status_code)

## Assim ficcou refatorada a a classe "SubscribePostTest":
class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='12345678901',
                    email='henrique@bastos.net', phone='21-99618-6180')

        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    ## Aqui estamos criando um teste para os e-mails enviandos.
    ## "mail.outbox" é um recurso interno do Django que ele usou para simular o envio de mails. Para isso ele foi na
    ## "views.py da App "subscriptions" e fez o código de simulação de envio de e-mails "mail.send_mail"
    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    ## Aqui estamos escrevendo um teste para a formatação dos e-mails, no caso o "Subject"
    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, email.subject)

    ## Aqui estamos escrevendo um teste para a formatação dos e-mails, no caso o "Remetente"
    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    ## Aqui estamos escrevendo um teste para a formatação dos e-mails, no caso o "Destinatário"
    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'henrique@bastos.net']

        self.assertEqual(expect, email.to)

    ## Aqui estamos escrevendo um teste para a formatação dos e-mails, no caso o CORPO DO E-MAIL"
    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Henrique Bastos', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('henrique@bastos.net', email.body)
        self.assertIn('21-99618-6180', email.body)

class SubscribeInvalidPost(TestCase):
    # def test_post(self):
    #     """Invalid POST should not redirect"""
    #     response = self.client.post('/inscricao/', {}) ## aqui estamos passando um dicionario vazio, simulnaod que não
    #                                                     ## foi preenchido nenhum campo em nosso formulario
    #     self.assertEqual(200, response.status_code)

    ## Despois de refatorado:
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_has_errors(self): ## aqui garantindo que quando tem erros, que estes erros sejam mostrados!
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Henrique Bastos', cpf='12345678901',
                    email='henrique@bastos.net', phone='21-99618-6180')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com Sucesso!')