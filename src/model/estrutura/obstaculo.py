from model.estrutura.resultadoInteracao import ResultadoInteracao

class Obstaculo:
    def __init__(self, tipo, p_inicial, p_final) -> None:
        self.tipo = tipo
        self.posicao = self.setObstaculo(p_inicial, p_final)


    def setObstaculo(self, p_inicial: tuple, p_final: tuple):
        posicao = []
            
        x_min = min(p_inicial[0], p_final[0])
        x_max = max(p_inicial[0], p_final[0])

        y_min = min(p_inicial[1], p_final[1])
        y_max = max(p_inicial[1], p_final[1])
        
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                posicao.append((x, y))

        return posicao

    def interagir(self):
        nova_posicao = False
        recompensa = None
        finalizado = None
        completado = None
        if self.tipo.lower() == "parede":
            nova_posicao = False
            recompensa = -10


        resultado = ResultadoInteracao(nova_posicao, recompensa, finalizado, completado)

        return resultado