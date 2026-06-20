from app import db
from models.admin import Admin

class AdminRepository:
    @staticmethod
    def add(admin):
        db.session.add(admin)
        db.session.commit()
        return admin
    
    @staticmethod
    def get_all():
        return Admin.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Admin.query.get(id)
    
    @staticmethod
    def get_by_email(email):
        return Admin.query.filter_by(email=email).first()
    
    @staticmethod
    def update(id, dados):
        admin = Admin.query.get(id)
        if admin:
            if 'nome' in dados:
                admin.nome = dados['nome']
            if 'email' in dados:
                admin.email = dados['email']
            if 'senha' in dados:
                admin.senha = dados['senha']
            db.session.commit()
            return admin
        return None
    
    @staticmethod
    def delete(id):
        admin = Admin.query.get(id)
        if admin:
            db.session.delete(admin)
            db.session.commit()
            return True
        return False