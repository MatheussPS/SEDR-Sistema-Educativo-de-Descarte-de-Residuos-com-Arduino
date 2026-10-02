class ColisaoService:

    def verificar_colisao(self, residuo, lixeira, sessao):
        
        if residuo.rect.colliderect(lixeira.rect):
            
            if residuo.tipo == lixeira.tipo and residuo.ativo:
            
                sessao.atualizar_pontuacao(5)

            elif residuo.tipo != lixeira.tipo and residuo.ativo:
            
                sessao.decrementar_vidas()
           
            residuo.ativo = False
            
            return True

            
        return False