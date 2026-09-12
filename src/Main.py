from model.Agente import Agente
from model.Ambiente import Ambiente
from model.estrutura.Obstaculo import *
from data.Excel import *

# import plotly.express as px

ambiente = Ambiente()
agente = Agente(ambiente.qtd_x, ambiente.qtd_y, ambiente.acoes)

num_chamada = 0

limite_passos = ambiente.objetivo['x'] + ambiente.objetivo['y'] + 3
janela_verificacao = 20

lista_sucessos = []
lista_quick = []

historico_completo = []
historico_fatiado = []
historico_avaliacao = []

def treino(epsilon = 0.1):
    global num_chamada
    num_chamada += 1
    historico_passos = []
    qtable_list = []

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
        passos = ""
        qtable = ""
        contador = 0

        # Looping EPISODIOS
        while not ambiente.isFinished():
            estado_anterior = estado

            acao = agente.escolher_acao()

            if acao == "up":
                passo = "↑" 
            elif acao == "down":
                passo = "↓" 
            elif acao == "right":
                passo = "→" 
            elif acao == "left":
                passo = "←" 

            novo_estado, recompensa, fim = ambiente.step(acao)
            print(recompensa)
            agente.QUpdate(estado_anterior, acao, recompensa, novo_estado)
            agente.estado = novo_estado

            estado = novo_estado

            passos += f"{contador}: Episodio: {eps_percorridos} | Posição: {estado_anterior} | Ação: {passo} | Nova Posição: {novo_estado}\n" #type:ignore
            qtable += f"{contador}: Episodio: {eps_percorridos} | Estado: {agente.estado} - {agente.QTable[agente.estado]}\n"
            contador += 1

        historico_passos.append(passos)
        qtable_list.append(qtable)
        qtable_list.append("-"*110+"\n")
        
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

    salvar_qtable(qtable_list)
    salvar_passos(historico_passos)
    # print(eps_percorridos)


def avaliacao():
    agente.setEpsilon(0)
    success = 0

    for x in range(100):
        estado = ambiente.reset()
        agente.reset()
        while not ambiente.isFinished() and agente.passos < 1000:
            estado_anterior = estado

            acao = agente.escolher_acao()


            novo_estado, recompensa, fim = ambiente.step(acao)
            agente.estado = novo_estado

            estado = novo_estado

        if ambiente.isFinished():
            success += 1

        historico_avaliacao.append(agente.passos)

    print(success)


obstaculo = Obstaculo("Parede", (3, 4), (5, 4))
ambiente.criar_obstaculo(obstaculo)

print(ambiente.obstaculos[0].posicao)
# print(obstaculo)


epsilon = 0.1
for x in range(1):
    epsilon -= (x*0.01) if epsilon > 0 else 0
    treino(epsilon)

# avaliacao()