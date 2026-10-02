class ColisaoService:

    def verificar_colisao(self, residuo, lixeira, sessao):
        
        if residuo.rect.colliderect(lixeira.rect):
            if residuo.tipo == lixeira.tipo and residuo.ativo:
                sessao.atualizar_pontuacao(5)
            elif residuo.tipo != lixeira.tipo and residuo.ativo:
                sessao.decrementar_vidas()
            # else:
            #     pontuacao -= 5
            residuo.ativo = False
            # print(sessao.pontuacao,
            # "RESIDUO:",
            # residuo.rect,
            # residuo.tipo,
            # "LIXEIRA:",
            # lixeira.rect,
            # lixeira.tipo, True
            # )
            return True

            
        return False