from django.contrib import messages
from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm

## Aqui eral assim antes dele usar o "IF" para tirar o fluxo do POST
# def subscribe(request):
#     # return HttpResponse() ## Este linha ele usou para fazer passar o teste e retornar o HttpResponse
#                           ## e depois, quando realmente foi utilizar o Template ele mudou para a linha abaixo
#                             ## Observar que apos isso o "import" do HttpResponse ficou cinxa na primeira linha
#                             ## eu não fiz aqui somente para deixar evidente o que fiz anteriormente, mas ele usou um recurso do
#                             # Pycham: "Code --> Optimize Imports" para otimizar os imports que não estão sendo mais usados
#     context = {'form': SubscriptionForm()}
#     return render(request, 'subscriptions/subscription_form.html', context)


def subscribe(request):
    if request.method == 'POST':

        ## Aqui está meio HardCod porque usou para fazer os testes. Agora, para CONECTAR nosso template de e-mail (com suas marcações a esta nossa VIEW) e pegar todos os dados
        ## já sanitizados do nosso Form, ele fez como abaixo (vide linha=27 à 30 e substituindo a linha 38 pela 39) tirando este "context' hardcoded pelos dados vindos do nosso formulário.
        # context = dict(name='Henrique Bastos', cpf='12345678901',
        #             email='henrique@bastos.net', phone='21-99618-6180')
        # body = render_to_string('subscriptions/subscription_email.txt', context)
        form = SubscriptionForm(request.POST)
        # form.full_clean() ## aqui ele cometou essa linha, pois após começar a trabalhar "Caso de Falha" (min: 19:25), ele muda o fluxo dos dados com o IF abaixo,
                            ## para testar que se os dados passados são validos
        if form.is_valid(): ## ----> Aqui pe caso de SUCESSO do Form.
            body = render_to_string('subscriptions/subscription_email.txt',
                                form.cleaned_data)
            mail.send_mail('Confirmação de inscrição',  ## Antes era "Subject". foi alterado para fazer o teste passar
                       # MESSAGE, ## antes aqui era 'Message', para resolver isso ele criou abaixo um TEMPLATE DE E-MAIL
                                  ## Apos criar o "Template de e-mail ele criou "body" onde tem as marcações dos campos!!!!
                       body, ## Que substitui MESSAGE, e que usa o templeta de e-mail com suas marcações, passando o "context" para comparação
                       'contato@eventex.com.br',    ## Antes era "sender@mail.com". foi alterado para fazer o teste passar
                       # ['contato@eventex.com.br', 'henrique@bastos.net']) ## Antes era "visitor@email.com". foi alterado para fazer o teste passar
                       ['contato@eventex.com.br', form.cleaned_data['email']]) ## Onde ['email'] é o nome do campo lá no nosso formulário


            messages.success(request, 'Inscrição realizada com Sucesso!')
            # Após ele criar o "Teste de Mensagens" no tests.py, ele veio aqui para "injetar"
            # esta mensagem. Ele também editou o template "subscriptions_form.html" e inseriu as linhas:
            # {% if messages %}
            #     {% for message in messages %}
            #         <div class="alert success">
            #         </div>
            #     {% endfor %}
            # {% endif %}

            # E também o seguinte na tag "head":
            # < style >
            # .alert
            # {
            #     padding: 0 15px;
            # margin - bottom: 1
            # rem;
            # border: 1
            # px
            # solid
            # transparent;
            # border - radius: .25
            # rem;
            # }
            # .alert
            # p
            # {
            #     padding: 7px 0 7px;
            # }
            # .alert.success
            # {
            #     color:  # 3c763d;
            #         background - color:  # dff0d8;
            # border - color:  # d0e9c6;
            # }
            # < / style >






            return HttpResponseRedirect('/inscricao/')
        else:  ## --> Aqui é caso de INSUCESSO/FALHA do Formulario
            return render(request, 'subscriptions/subscription_form.html',
                          {'form': form})


    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)


## Aqui etá o TEMPLATE DE E-MAIL: (que aṕos fazer o teste passar, ele criou o arquivo "subscription_mail.txt" e colou
## a esta mesagem lá dentro. OBSERVANDO QUE QUANDO ELE USA "Nome: {{ name }}" é igualzinho o nome dos campos que ele usou no formulário
# MESSAGE = """
# Olá! Tudo bem?
#
# Muito obrigada por se inscrever no Eventex.
#
# Estes foram os daods que você nos forneceu em sua incrição:
#
# Nome: Henrique Bastos
# CPF: 12345678901
# Email: henrique@bastos.net'
# Telefone: 21-99618-6180
#
# Em até 48 horas úteis a nossa equipe entrará en contato,
#
# Att,
# Morena
#
# """
