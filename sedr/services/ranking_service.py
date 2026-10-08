import os


class RankingService:
  
    
    def __init__(self, arquivo="pontuacao/pontuacoes.txt"):
        self.arquivo = arquivo
        # Cria a pasta pontuacoes se não existir
        pasta = os.path.dirname(self.arquivo)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta)
    
    def salvar_pontuacao(self, pontuacao):
  
        try:
            with open(self.arquivo, "a", encoding="utf-8") as f:
                f.write(f"{pontuacao}\n")
        except Exception as e:
            print(f"Erro ao salvar pontuação: {e}")
    
    def obter_pontuacoes(self):
      
        if not os.path.exists(self.arquivo):
            return []
        
        pontuacoes = []
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        try:
                            pontuacoes.append(int(linha))
                        except ValueError:
                            # Ignora linhas que não são números válidos
                            pass
        except Exception as e:
            print(f"Erro ao ler pontuações: {e}")
            return []
        
        # Ordena em ordem decrescente
        pontuacoes.sort(reverse=True)
        return pontuacoes
