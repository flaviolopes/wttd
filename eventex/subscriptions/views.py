from django.http import HttpResponse
from django.shortcuts import render

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    # return HttpResponse() ## Este linha ele usou para fazer passar o teste e retornar o HttpResponse
                          ## e depois, quando realmente foi utilizar o Template ele mudou para a linha abaixo
                            ## Observar que apos isso o "import" do HttpResponse ficou cinxa na primeira linha
                            ## eu não fiz aqui somente para deixar evidente o que fiz anteriormente, mas ele usou um recurso do
                            # Pycham: "Code --> Optimize Imports" para otimizar os imports que não estão sendo mais usados
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)
