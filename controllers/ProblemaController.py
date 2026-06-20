from flask import render_template
from models.problema import Problema

class ProblemaController:
    def __init__(self):
        self.model = Problema()
    
    def index(self):
        enunciado = "DESENVOLVIMENTO WEB II - Unidade 1 - Tarefa MVC"
        return render_template('index/index.html', enunciado=enunciado)
    
    def problema(self, dados=None):
        if dados:
            self.model.processar_formulario(dados)
            resultado = self.model.resolver_problema()
            return render_template('problema/problema.html',
                                 enunciado="Problema de Exemplo",
                                 resultado=resultado,
                                 dados_recebidos=dados)
        else:
            resultado = self.model.resolver_problema()
            return render_template('problema/problema.html',
                                 enunciado="Problema de Exemplo",
                                 resultado=resultado,
                                 dados_recebidos=None)