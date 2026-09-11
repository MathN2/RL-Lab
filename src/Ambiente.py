class Ambiente:
    def __init__(self):
        self.qtd_x = 10
        self.qtd_y = 10
        self.limite_x = 9
        self.limite_y = 9
        self.posicao = {'x': 0, 'y': 0}
        self.objetivo = {'x': 9, 'y': 7}
        self.qtd_posicoes = self.qtd_x * self.qtd_y

        self.acoes = [
            'up',
            'down',
            'left',
            'right'
        ]

        obstaculos = []

    def reset(self):
        self.posicao = {'x': 0, 'y': 0}
        return (self.posicao['x'], self.posicao['y'])

    def step(self, acao):
        posicao_anterior = self.posicao.copy()

        if acao == 'up':
            self.posicao['y'] += 1
        elif acao == 'down':
            self.posicao['y'] -= 1
        elif acao == 'right':
            self.posicao['x'] += 1
        elif acao == 'left':
            self.posicao['x'] -= 1

        self.posicao['x'] = max(0, min(self.posicao['x'], self.limite_x))
        self.posicao['y'] = max(0, min(self.posicao['y'], self.limite_y))


        if self.posicao['x'] > self.limite_x:
            self.posicao['x'] = self.limite_x

        if self.posicao['x'] < 0:
            self.posicao['x'] = 0
            
        if self.posicao['y'] > self.limite_y:
            self.posicao['y'] = self.limite_y

        if self.posicao['y'] < 0:
            self.posicao['y'] = 0


        if self.posicao == posicao_anterior:
            recompensa = -2
        else:
            recompensa = -1

        if self.posicao == self.objetivo:
            recompensa = 10


        finalizado = self.isFinished()

        return (self.posicao['x'], self.posicao['y']), recompensa, finalizado

    def isFinished(self):
        return self.posicao == self.objetivo

    def setObstaculos(self, p_inicial: tuple, p_final: tuple):
        obstaculo = []
        
        x_min = min(p_inicial[0], p_final[0])
        x_max = max(p_inicial[0], p_final[0])

        y_min = min(p_inicial[1], p_final[1])
        y_max = max(p_inicial[1], p_final[1])
        
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                obstaculo.append((x, y))

        return obstaculo


