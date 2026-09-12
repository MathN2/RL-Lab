import random

class Agente:
    def __init__(self, x, y, acoes_possiveis):
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1

        self.x = x
        self.y = y
        self.acoes_possiveis = acoes_possiveis

        self.passos = 0
        self.estado: tuple[int, int] = (0, 0)
        self.QTable = {}

        self.SetQTable()

    def SetQTable(self):
        for x in range(self.x):
            for y in range(self.y):
                self.QTable[(x, y)] = {}
            
                for acao in self.acoes_possiveis:
                    self.QTable[(x, y)][acao] = 0


    def setEpsilon(self, epsilon):
        self.epsilon = epsilon
    

    def reset(self):
        self.passos = 0
        self.estado = (0, 0)

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


    def QUpdate(self, estado, acao, recompensa, novo_estado):
        valor_atual = self.QTable[estado][acao]

        melhor_futuro = max(self.QTable[novo_estado].values())
        Qnovo = valor_atual + self.alpha * (recompensa + self.gamma * melhor_futuro - valor_atual)

        self.QTable[estado][acao] = Qnovo
    