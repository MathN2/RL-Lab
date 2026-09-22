import random

class Agente:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.estado_atual
        self.acoes_possiveis = []

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        self.QTable = {}

        self.passos = 0

        self.set_qtable()


    # -- TIPOS DE RESET -----------------------------
    def reset(self):
        self.passos = 0
        self.estado = self.posicao_inicial.copy()

    def hard_reset(self):
        self.reset()
        self.set_qtable()


    # -- CONFIGURAÇOES QTABLE --------------------------
    def set_qtable(self):
        for x in range(self.qtd_x):
            for y in range(self.qtd_y):
                self.QTable[(x, y)] = {}
            
                for acao in self.acoes_possiveis:
                    self.QTable[(x, y)][acao] = 0


    def QUpdate(self, estado, acao, recompensa, novo_estado):
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
    def configurar_ambiente(self, ambiente):
        pass
    
    # -- CONFIGURAÇOES DE AÇOES -----------------------
    def configurar_acoes(self, novas_acoes):
        self.acoes_possiveis = novas_acoes

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
        valor = max(self.QTable[self.estado].values())
        keys = [k for k, v in self.QTable[self.estado].items() if v == valor]

        return random.choice(keys)


    
    