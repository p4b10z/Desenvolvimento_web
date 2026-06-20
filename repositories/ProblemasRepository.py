from app import db
from models.problema import Problema

class ProblemaRepository:
    @staticmethod
    def add(problema):
        db.session.add(problema)
        db.session.commit()
        return problema
    
    @staticmethod
    def get_all():
        return Problema.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Problema.query.get(id)
    
    @staticmethod
    def update(id, dados):
        problema = Problema.query.get(id)
        if problema:
            if 'titulo' in dados:
                problema.titulo = dados['titulo']
            if 'descricao' in dados:
                problema.descricao = dados['descricao']
            if 'dados' in dados:
                problema.dados = dados['dados']
            if 'resultado' in dados:
                problema.resultado = dados['resultado']
            db.session.commit()
            return problema
        return None
    
    @staticmethod
    def delete(id):
        problema = Problema.query.get(id)
        if problema:
            db.session.delete(problema)
            db.session.commit()
            return True
        return False