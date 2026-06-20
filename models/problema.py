class Problema:
    def __init__(self):
        self.dados = []
        self.resultado = ""
    
    def resolver_problema(self):
        if self.dados:
            try:
                numeros = [int(x.strip()) for x in self.dados.split(',')]
                soma = sum(numeros)
                self.resultado = f"Soma dos números {numeros} = {soma}"
            except:
                self.resultado = "Erro ao processar os dados. Use números separados por vírgula."
        else:
            self.resultado = "Solução do problema calculada com sucesso!"
        
        return self.resultado
    
    def processar_formulario(self, dados):
        self.dados = dados
        return True