class ResultadoInteracao:
    def __init__(self, nova_posicao: tuple | bool = False, recompensa: int | None = None, finalizado: bool | None = None):
        self.nova_posicao = nova_posicao
        self.recompensa = recompensa
        self.finalizado = finalizado