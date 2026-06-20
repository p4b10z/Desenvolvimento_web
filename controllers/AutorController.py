from flask import render_template

class AutorController:
    
    def autor(self):
        dados_autor = {
            'nome': 'Seu Nome Aqui',
            'formacoes': [
                'Análise e Desenvolvimento de Sistemas',
                'Desenvolvimento Web - Flask',
                'Curso de Python Avançado'
            ],
            'experiencias': [
                'Desenvolvedor Web - Projeto X',
                'Estagiário em Desenvolvimento - Empresa Y',
                'Projeto Acadêmico - Sistema de Gestão'
            ]
        }
        return render_template('autor/autor.html', autor=dados_autor)