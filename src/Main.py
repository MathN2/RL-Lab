# Package
from model.Agente import Agente
from model.Ambiente import Ambiente
from model.estrutura.Obstaculo import *
from data.Excel import *

# Libraries
from statistics import median
# import plotly.express as px


# -- Configuração --------------------------------------------------
ambiente = Ambiente()
agente = Agente(ambiente.qtd_x, ambiente.qtd_y, ambiente.acoes)

obstaculo = Obstaculo("Parede", (4, 0), (4, 6))
ambiente.criar_obstaculo(obstaculo)
obstaculo = Obstaculo("Parede", (4, 6), (6, 6))
ambiente.criar_obstaculo(obstaculo)
obstaculo = Obstaculo("Parede", (6, 6), (6, 1))
ambiente.criar_obstaculo(obstaculo)
#-----------------------------------------------------------------

num_chamada = 0
janela_verificacao = 20
limite_episodios = 10000

def treino(epsilon = 0.1):
    global num_chamada
    num_chamada += 1
    num_ciclo = 0
    eps_percorridos = 1

    agente.epsilon = epsilon
    planilha, sheet = criar_sheet(f"Execução {num_chamada}")

    minimo_passos = ambiente.bfs_calc()
    if minimo_passos is None:
        return None

    historico_completo = []
    historico_fatiado = []
    historico_passos = []
    qtable_list = []

    eficiencia = 0
    eficiencia_minima = 95

    while True:
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
            agente.QUpdate(estado_anterior, acao, recompensa, novo_estado)
            agente.estado = novo_estado

            estado = novo_estado

            passos += f"{contador}: Episodio: {eps_percorridos} | Posição: {estado_anterior} | Ação: {passo} | Nova Posição: {novo_estado}\n" #type:ignore
            qtable += f"{contador}: Episodio: {eps_percorridos} | Estado: {agente.estado} - {agente.QTable[agente.estado]}\n"
            contador += 1

        qtable_list.append(qtable)
        qtable_list.append("-"*110+"\n")
        
        historico_passos.append(passos)
        historico_completo.append(agente.passos)
        
        eficiencia = (minimo_passos / agente.passos) * 100

        if eficiencia >= eficiencia_minima:
            historico_fatiado.append(historico_completo[num_ciclo * janela_verificacao:])
            valor_salvar = num_ciclo + 0.5
            finalizar = True

        elif eps_percorridos % janela_verificacao == 0 and eps_percorridos != 0:
            num_ciclo += 1
            
            historico_fatiado.append(historico_completo[-janela_verificacao:])
            valor_salvar = num_ciclo
            finalizar = False

        else:
            valor_salvar = None
            finalizar = False

        if valor_salvar is not None:
            historico_atual = historico_fatiado[-1]
            media = sum(historico_atual) / len(historico_atual)
            mediana = median(historico_atual)
            menor = min(historico_atual)
            maior = max(historico_atual)

            salvar(planilha, sheet, valor_salvar, media, mediana, menor, maior, eficiencia)


        if num_ciclo > 100:
            agente.epsilon -= 0.01
        
        eps_percorridos += 1

        if finalizar or eps_percorridos > limite_episodios:
            break

    salvar_qtable(qtable_list)
    salvar_passos(historico_passos)


def avaliacao():
    agente.setEpsilon(0)
    success = 0

    historico_avaliacao = []

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


epsilon = 0.1
for x in range(5):
    epsilon -= (x*0.01) if epsilon > 0 else 0
    treino(epsilon)

# avaliacao()