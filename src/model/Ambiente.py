from model.estrutura.Obstaculo import *
from model.estrutura.ResultadoInteracao import *

from collections import deque

class Ambiente:
    def __init__(self, limite_inferior=(0, 0), limite_superior=(9,9)):
        #Validação dos limites
        if (
            limite_superior[0] < limite_inferior[0]
            or limite_superior[1] < limite_inferior[1]
        ):
            raise ValueError

        self.qtd_x = 11
        self.qtd_y = 11

        self.limite_inferior = (0, 0)
        self.limite_superior = (10, 10)

        self.posicao_inicial = {'x': 0, 'y': 0}
        self.posicao = self.posicao_inicial.copy()
        self.objetivo = {'x': 5, 'y': 5}
        self.qtd_posicoes = self.qtd_x * self.qtd_y

        self.acoes = [
            'up',
            'down',
            'left',
            'right'
        ]

        self.obstaculos = []

    def get_posicao_tupla(self):
        posicao = (self.posicao['x'], self.posicao['y'])
        return posicao

    def set_posicao_tupla(self, posicao):
        self.posicao['x'] = posicao[0]
        self.posicao['y'] = posicao[1]

    def reset(self):
        self.posicao = self.posicao_inicial.copy()
        return (self.posicao['x'], self.posicao['y'])

    def isFinished(self):
        return self.posicao == self.objetivo

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

        self.posicao['x'] = max(0, min(self.posicao['x'], self.limite_superior[0]))
        self.posicao['y'] = max(0, min(self.posicao['y'], self.limite_superior[1]))

        if self.posicao == posicao_anterior:
            recompensa = -2
        else:
            recompensa = -1

        if self.posicao == self.objetivo:
            recompensa = 10

        resultado= self.verificar_interacao()
        if resultado is not None:
            posicao_atual = (posicao_anterior['x'], posicao_anterior['y']) if resultado.nova_posicao == False else self.get_posicao_tupla()
            self.posicao['x'] = posicao_atual[0]
            self.posicao['y'] = posicao_atual[1]

            recompensa = resultado.recompensa
            finalizado = resultado.finalizado
            
        else:
            posicao_atual = self.get_posicao_tupla()
            finalizado = self.isFinished()

        return posicao_atual, recompensa, finalizado


    def criar_obstaculo(self, obstaculo:Obstaculo):
        x_min = min(ob[0] for ob in obstaculo.posicao)
        x_max = max(ob[0] for ob in obstaculo.posicao)
        y_min = min(ob[1] for ob in obstaculo.posicao)
        y_max = max(ob[1] for ob in obstaculo.posicao)

        if (
            x_min < self.limite_inferior[0] or
            x_max > self.limite_superior[0] or
            y_min < self.limite_inferior[1] or
            y_max > self.limite_superior[1]
        ):
            return None

        self.obstaculos.append(obstaculo)


    def verificar_interacao(self) -> ResultadoInteracao | None:
        for obstaculo in self.obstaculos:
            if self.get_posicao_tupla() in obstaculo.posicao:
                resultado: ResultadoInteracao = obstaculo.interagir()
                return resultado
        return None


    def bfs_calc(self):
        atual = (self.posicao_inicial['x'], self.posicao_inicial['y'])
        objetivo = (self.objetivo['x'], self.objetivo['y'])
        acoes = self.acoes

        fila = deque([atual])
        visitados = set()
        distancias = {atual: 0}
        obstaculos = self.obstaculos

        visitados.add(atual)

        while fila:
            atual = fila.popleft()

            if atual == objetivo:
                return distancias[atual]

            for acao in acoes:
                acao = acao.lower()
                bloqueado = False
                dx = dy = 0

                if acao == "up" and atual[1] != self.limite_superior[1]:
                    dy = 1

                elif acao == "down" and atual[1] != self.limite_inferior[1]:
                    dy = -1

                elif acao == "right" and atual[0] != self.limite_superior[0]:
                    dx = 1

                elif acao == "left" and atual[0] != self.limite_inferior[0]:
                    dx = -1
                else:
                    continue


                vizinho = (atual[0] + dx, atual[1] + dy)

                bloqueado = any(vizinho in obstaculo.posicao for obstaculo in obstaculos)

                if not bloqueado and vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
                    distancias[vizinho] = distancias[atual] + 1

        return None