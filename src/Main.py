# Package
from model.Agente import Agente
from model.Ambiente import Ambiente
from model.estrutura.Obstaculo import Obstaculo
from data.Excel import criar_sheet, salvar_resultados, salvar_passos, salvar_qtable, salvar_execucao

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
#------------------------------------------------------------------

num_chamada = 0
janela_verificacao = 10
limite_episodios = 10000

acoes = {   # acoes é um recurso temporario para logs
        'up': "↑",
        'down': "↓",
        'left': "←",
        'right': "→",
    }


def treinar(epsilon = 0.1):
    global num_chamada, num_ep
    num_chamada += 1
    num_ciclo = 0
    num_ep = 1
    num_total_completos = 0
    num_completos = 0

    agente.epsilon = epsilon
    planilha, sheet = criar_sheet(f"Execução {num_chamada}")

    minimo_passos = ambiente.bfs_calc()
    if minimo_passos is None:
        return None

    historico_completo = []
    historico_eficiencia = []
    historico_passos = []
    historico_convergencia = []
    qtable_list = []

    eficiencia = 0

    while True:
        estado = ambiente.reset()
        agente.reset()

        # Looping EPISODIOS
        passos, qtable, completo = executar_episodio(ambiente, agente, estado, True)

        if completo:
            num_completos += 1
            eficiencia = (minimo_passos / agente.passos) * 100
        else:
            eficiencia = 0

        qtable_list.append(qtable)
        qtable_list.append("-"*170+"\n")
        
        passos += "-"*100+"\n"
        historico_passos.append(passos)
        historico_completo.append(agente.passos)
        historico_eficiencia.append(eficiencia)
        

        # CICLO
        if num_ep % janela_verificacao == 0:
            num_ciclo += 1

            if num_ciclo != 0 and num_ciclo % 10 == 0:
                agente.epsilon = max(0, agente.epsilon - 0.01)
            
            historico_atual = historico_completo[-janela_verificacao:]
            eficiencia_ciclo = historico_eficiencia[-janela_verificacao:]
            ciclo_id = num_ciclo

            historico_convergencia.append(avaliar(minimo_passos))

        else:
            ciclo_id = None
            historico_atual = None

        if ciclo_id is not None:
            salvar_estatisticas(planilha, sheet, ciclo_id, historico_atual, eficiencia_ciclo, num_completos)
            num_total_completos += num_completos
            num_completos = 0

        num_ep += 1

        if len(historico_convergencia) >= 5:
            if all(historico_convergencia[-5:]):
                break

    # CRIAR SALVAR TOTAL
    prep_salvar_execucao(epsilon, num_ep, num_ciclo, num_total_completos, historico_eficiencia, historico_completo)
    salvar_qtable(qtable_list)
    salvar_passos(historico_passos)


def avaliar(minimo_passos):
    agente.setEpsilon(0)
    success = 0
    limite = minimo_passos * 10

    historico_avaliacao = []
    historico_eficiencia = []

    for x in range(100):
        cont = 0
        estado = ambiente.reset()
        agente.reset()

        executar_episodio(ambiente, agente, estado, True)

        if ambiente.isFinished():
            eficiencia = (minimo_passos / agente.passos) * 100
            finalizou = True
        else:
            eficiencia = 0
            finalizou = False

        historico_avaliacao.append({x: [agente.passos, finalizou]})
        historico_eficiencia.append(eficiencia)

    for e in historico_eficiencia:
        if e >= 95:
            success += 1

    media = sum(historico_eficiencia) / len(historico_eficiencia)

    if success >= (len(historico_eficiencia) * 0.9) and media > 95:
        return True
    else:
        return False


def executar_episodio(ambiente:Ambiente, agente:Agente, estado, treinar=False):  
    global acoes
    contador = 1
    completo = True
    passos = ""
    qtable = ""
    

    while not ambiente.isFinished():
        estado_anterior = estado
            
        acao = agente.escolher_acao()
    
        novo_estado, recompensa, fim = ambiente.step(acao)
        estado = novo_estado
        agente.estado = novo_estado
    
        if treinar:
            agente.QUpdate(estado_anterior, acao, recompensa, novo_estado)

        # Logs
        passos += f"{str(contador).center(5)}: Episodio: {num_ep} | Posição: {str(estado_anterior).center(10)} | Ação: {acoes[acao]} | Nova Posição: {str(estado).center(8)}\n"
        qtable += f"{str(contador).center(5)}: Episodio: {num_ep} | Estado: {str(agente.estado).center(5)} - {str(agente.QTable[agente.estado]).center(120)}\n"
        contador += 1

        if fim:
            completo = False
            break

    return passos, qtable, completo


def prep_salvar_execucao(epsilon, episodios, ciclos, completados, historico_eficiencia, historico_completo):
    eficiencia_media = sum(historico_eficiencia) / len(historico_eficiencia)
    taxa_completos = (completados / episodios) * 100
    passos_media = sum(historico_completo) / len(historico_completo)

    # epsilon_inicial, episodios, ciclos, completados, taxa_comp, eficiencia, passos, resultado
    salvar_execucao(str(epsilon), episodios, ciclos, completados, taxa_completos, eficiencia_media, passos_media)

def salvar_estatisticas(planilha, sheet, ciclo_id, historico, eficiencia_ciclo, num_completos):
    eficiencia_media = sum(eficiencia_ciclo) / len(eficiencia_ciclo)
    media = sum(historico) / len(historico)
    mediana = median(historico)
    menor = min(historico)
    maior = max(historico)
    percentual_completos = (num_completos / janela_verificacao) * 100

    salvar_resultados(planilha, sheet, ciclo_id, media, mediana, menor, maior, eficiencia_media, percentual_completos)


epsilon = 0.1
for x in range(1):
    agente.hard_reset()
    epsilon = 0.1 - (x*0.01) if epsilon > 0 else 0
    treinar(epsilon)