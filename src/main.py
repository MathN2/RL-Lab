# Package
from model.agente import Agente
from model.ambiente import Ambiente
from model.estrutura.obstaculo import Obstaculo
from persistencia import criar_sheet, salvar_resultados, salvar_passos, salvar_qtable, salvar_execucao

# Libraries
from statistics import median
# import plotly.express as px


# -- Configuração l1 --------------------------------------------------
level1 = Ambiente()
agente = Agente()
# level1.qtd_x, level1.qtd_y, level1.acoes

obstaculo = Obstaculo("Parede", (4, 0), (4, 6))
level1.criar_obstaculo(obstaculo)
obstaculo = Obstaculo("Parede", (4, 6), (6, 6))
level1.criar_obstaculo(obstaculo)
obstaculo = Obstaculo("Parede", (6, 6), (6, 1))
level1.criar_obstaculo(obstaculo)
#----------------------------------------------------------------------

# -- Configuração l2 --------------------------------------------------
level2 = Ambiente((0, 0), (20, 15))

# -- Treinamento.py ---------------------------------------------------
num_chamada = 0
janela_verificacao = 10
limite_episodios = 10000

acoes = {   # acoes é um recurso temporario para logs
        'up': "↑",
        'down': "↓",
        'left': "←",
        'right': "→",
    }


def treinar(alpha, gamma, epsilon):
    global num_chamada, num_ep
    num_chamada += 1
    num_ciclo = 0
    num_ep = 0
    num_total_completos = 0
    num_completos = 0

    agente.set_alpha = alpha
    agente.set_gamma = gamma
    agente.set_epsilon = epsilon
    planilha, sheet = criar_sheet(f"Execução {num_chamada}")

    minimo_passos = level1.bfs_calc()
    if minimo_passos is None:
        return None

    historico_completo = []
    historico_eficiencia = []
    historico_passos = []
    historico_convergencia = []
    qtable_list = []

    eficiencia = 0

    while True:
        estado = level1.reset()
        agente.reset()

        # Looping EPISODIOS
        passos, qtable, completo = executar_episodio(level1, agente, estado, True)

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
    prep_salvar_execucao(alpha, gamma, epsilon, num_ep, num_ciclo, num_total_completos, historico_eficiencia, historico_completo)
    salvar_qtable(qtable_list)
    salvar_passos(historico_passos)


def avaliar(minimo_passos):
    agente.set_epsilon(0)
    success = 0

    historico_avaliacao = []
    historico_eficiencia = []

    for x in range(100):
        estado = level1.reset()
        agente.reset()

        executar_episodio(level1, agente, estado, True)

        if level1.is_finished():
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


def executar_episodio(level1:Ambiente, agente:Agente, estado, treinar=False):  
    global acoes
    contador = 1
    completo = True
    passos = ""
    qtable = ""
    

    while not level1.is_finished():
        estado_anterior = estado
            
        acao = agente.escolher_acao()
    
        novo_estado, recompensa, fim = level1.step(acao)
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


def prep_salvar_execucao(alpha, gamma, epsilon, episodios, ciclos, completados, historico_eficiencia, historico_completo):
    eficiencia_media = sum(historico_eficiencia) / len(historico_eficiencia)
    taxa_completos = (completados / episodios) * 100
    passos_media = sum(historico_completo) / len(historico_completo)

    # epsilon_inicial, episodios, ciclos, completados, taxa_comp, eficiencia, passos, resultado
    salvar_execucao(alpha, gamma, str(epsilon), episodios, ciclos, completados, taxa_completos, eficiencia_media, passos_media)

def salvar_estatisticas(planilha, sheet, ciclo_id, historico, eficiencia_ciclo, num_completos):
    eficiencia_media = sum(eficiencia_ciclo) / len(eficiencia_ciclo)
    media = sum(historico) / len(historico)
    mediana = median(historico)
    menor = min(historico)
    maior = max(historico)
    percentual_completos = (num_completos / janela_verificacao) * 100

    salvar_resultados(planilha, sheet, ciclo_id, media, mediana, menor, maior, eficiencia_media, percentual_completos)


# Recomendações:
# - epsilon: normalmente faz sentido iniciar mais alto e reduzir ao longo das execuções.
# - alpha: pode ser incrementado ou reduzido dependendo do experimento.
# - gamma: normalmente deve permanecer entre 0 e 1.
# - incrementos são percentuais e devem estar entre 0 e 1.

conf = {
    "resetar_Qtable": False,
    "qtd_execucoes": 10,

    "valores": {
        "alpha": {
                "valor": 0.1,
                "incrementar_global": False,
                "incremento": 0
        },
    
        "gamma": {
            "valor": 0.9,
            "incrementar_global": False,
            "incremento": 0.01
        },
    
        "epsilon": {
            "valor": 0.1,
            "incrementar_global": True,
            "incremento": 0
        }
    },
    
    "incremento_global": 0.1
}

def validar_configuracao(conf):
    for valor in conf["valores"].values():
        if not 0 <= valor["valor"] <= 1:
            raise ValueError("Alpha, gamma e epsilon devem estar entre 0 e 1.")

        if not -1 <= valor["incremento"] <= 1:
            raise ValueError("O incremento deve estar entre -1 e 1.")

        if not -1 <= conf["incremento_global"] <= 1:
            raise ValueError("O incremento global deve estar entre -1 e 1.")
        

def atualizar_configuracao(conf):
    for valor in conf["valores"].values():    
        if valor["incrementar_global"]:
            incremento = conf["incremento_global"]
        else:
            incremento = valor["incremento"]

        novo_valor =  valor["valor"] * (1 + incremento)

        if not 0 <= novo_valor <= 1:
            raise ValueError("O incremento ultrapassou os limites do parâmetro.")
        else:
            valor["valor"] = novo_valor

        valor["valor"] = max(0, (min(1, valor["valor"])))


def executar_experimento(conf):
    validar_configuracao(conf)

    for x in range(conf["qtd_execucoes"]):
        alpha = conf["valores"]["alpha"]["valor"]
        gamma = conf["valores"]["gamma"]["valor"]
        epsilon = conf["valores"]["epsilon"]["valor"]

        treinar(alpha, gamma, epsilon)

        atualizar_configuracao(conf)
        
        if conf["resetar_Qtable"]:
            agente.hard_reset()
            
executar_experimento(conf)