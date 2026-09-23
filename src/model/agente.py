import random

class Agente:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.estado_atual = None
        self.ambiente_atual = None
        self.acoes_possiveis = []

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.QTable = {}

        self.passos = 0


    # -- TIPOS DE RESET -----------------------------
    def reset(self):
        self.passos = 0
        self.estado_atual = self.ambiente_atual.reset()
        self.set_qtable(self.estado_atual)

    def hard_reset(self):
        self.reset()
        self.QTable = {}


    # -- CONFIGURAÇOES QTABLE --------------------------
    def set_qtable(self, novo_estado):
        if not novo_estado in self.QTable:
            self.QTable[novo_estado] = {}

            for acao in self.acoes_possiveis:
                self.QTable[novo_estado][acao] = 0


    def QUpdate(self, estado, acao, recompensa, novo_estado):
        self.set_qtable(novo_estado)
        valor_atual = self.QTable[estado][acao]

        melhor_futuro = max(self.QTable[novo_estado].values())
        Qnovo = valor_atual + self.alpha * (recompensa + self.gamma * melhor_futuro - valor_atual)

        self.QTable[estado][acao] = Qnovo

    
    # -- CONFIGURAÇOES HIPERPARAMETROS ----------------
    def set_alpha(self, alpha):
        self.alpha = alpha
    def set_gamma(self, gamma):
        self.gamma = gamma
    def set_epsilon(self, epsilon):
        self.epsilon = epsilon


    # -- CONFIGURAÇOES AMBIENTE -----------------------
    def entrar_ambiente(self, ambiente):
        self.ambiente_atual = ambiente
        self.configurar_acoes()
        self.reset()
    
    # -- CONFIGURAÇOES DE AÇOES -----------------------
    def configurar_acoes(self):
        self.acoes_possiveis = self.ambiente_atual.acoes

    def add_acao(self, acao):
        if not acao in self.acoes_possiveis:
            self.acoes_possiveis.append(acao)

    def remover_acao(self, acao):
        if acao in self.acoes_possiveis:
            self.acoes_possiveis.remove(acao)

    
    #  -- DECISOES DO AGENTE ------------------------
    def escolher_acao(self):
        if random.random() < self.epsilon:
            acao = self.acao_exploratoria()
        else:
            acao = self.acao_greedy()

        self.passos += 1
        return acao
    

    def acao_exploratoria(self):
        return random.choice(self.acoes_possiveis)
    

    def acao_greedy(self):
        valor = max(self.QTable[self.estado_atual].values())
        keys = [k for k, v in self.QTable[self.estado_atual].items() if v == valor]

        return random.choice(keys)
    