class ColisaoService:

    def __init__(self, ao_acertar=None):
        # Função opcional chamada UMA vez a cada descarte correto.
        # Recebe a lixeira em que o resíduo foi descartado.
        self.ao_acertar = ao_acertar

    def verificar_colisao(self, residuo, lixeira, sessao):
        
        if residuo.rect.colliderect(lixeira.rect):
            
            if residuo.tipo == lixeira.tipo and residuo.ativo:
                # Acertou a lixeira correta - ganha pontos
                sessao.atualizar_pontuacao(5)

                # Avisa quem precisa reagir ao acerto (ex.: acender o LED)
                if self.ao_acertar is not None:
                    self.ao_acertar(lixeira)

            elif residuo.tipo != lixeira.tipo and residuo.ativo:
                # Errou a lixeira - apenas perde vida
                sessao.decrementar_vidas()
           
            residuo.ativo = False
            
            return True

            
        return False