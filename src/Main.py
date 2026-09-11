from Agente import Agente
from Ambiente import Ambiente
from Excel import *

# import plotly.express as px

ambiente = Ambiente()
agente = Agente(ambiente.qtd_x, ambiente.qtd_y, ambiente.acoes)

num_chamada = 0

limite_passos = ambiente.objetivo['x'] + ambiente.objetivo['y'] + 3
janela_verificacao = 100

lista_sucessos = []
lista_quick = []

historico_completo = []
historico_fatiado = []
historico_avaliacao = []

def treino(epsilon = 0.1):
    global num_chamada
    num_chamada += 1

    planilha, sheet = criar_sheet(f"Execução {num_chamada}")
    agente.epsilon = epsilon

    sucessos = 0
    quick_sucessos = 0

    percentual_sucessos = 0
    percentual_rapidos = 0

    eps_percorridos = 1
    num_ciclo = 0

    while percentual_rapidos < 98:
        estado = ambiente.reset()
        agente.reset()

        while not ambiente.isFinished():
            estado_anterior = estado

            acao = agente.escolher_acao()

            novo_estado, recompensa, fim = ambiente.step(acao)
            agente.QUpdate(estado_anterior, acao, recompensa, novo_estado)
            agente.estado = novo_estado

            estado = novo_estado


        if ambiente.isFinished():
            sucessos += 1
            if agente.passos <= limite_passos:
                quick_sucessos += 1

    
        historico_completo.append(agente.passos)

        if eps_percorridos % janela_verificacao == 0 and eps_percorridos != 0:
            lista_sucessos.append(sucessos)
            lista_quick.append(quick_sucessos)

            percentual_sucessos = sucessos / janela_verificacao * 100
            percentual_rapidos = quick_sucessos / janela_verificacao * 100

            sucessos = quick_sucessos = 0
            num_ciclo += 1

            historico_fatiado.append(historico_completo[-100:])

            media = sum(historico_fatiado[-1]) / janela_verificacao
            mediana = historico_fatiado[-1][int(len(historico_fatiado[-1]) / 2)]
            minimo = min(historico_fatiado[-1])
            maximo = max(historico_fatiado[-1])

            salvar(planilha, sheet, num_ciclo, media, mediana, minimo, maximo, percentual_rapidos)

        if num_ciclo > 100:
            agente.epsilon -= 0.01
            print(num_ciclo)
        
        eps_percorridos += 1


def avaliacao():
    agente.setEpsilon(0)
    success = 0

    for x in range(100):
        estado = ambiente.reset()
        agente.reset()
        while not ambiente.isFinished() and agente.passos < 1000:
            estado_anterior = estado

            acao = agente.escolher_acao()
            # print(agente.estado)
            # print(acao)

            novo_estado, recompensa, fim = ambiente.step(acao)
            agente.estado = novo_estado

            estado = novo_estado

        if ambiente.isFinished():
            success += 1

        historico_avaliacao.append(agente.passos)

    print(success)

epsilon = 0.1
for x in range(5):
    epsilon -= (x*0.01) if epsilon > 0 else 0
    treino(epsilon)

avaliacao()