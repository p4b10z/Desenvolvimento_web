from flask import request, jsonify
from app import Admin, AdminRepository

class AdminController:
    @staticmethod
    def get_all():
        admins = AdminRepository.get_all()
        return jsonify([a.to_dict() for a in admins])
    
    @staticmethod
    def get_by_id(id):
        admin = AdminRepository.get_by_id(id)
        if admin:
            return jsonify(admin.to_dict())
        return jsonify({'erro': 'Administrador não encontrado'}), 404
    
    @staticmethod
    def create():
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Dados inválidos'}), 400
        
        if not dados.get('nome') or not dados.get('email'):
            return jsonify({'erro': 'Nome e email são obrigatórios'}), 400
        
        admin = Admin(
            nome=dados.get('nome', ''),
            email=dados.get('email', ''),
            senha=dados.get('senha', '')
        )
        AdminRepository.add(admin)
        return jsonify(admin.to_dict()), 201
    
    @staticmethod
    def update(id):
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Dados inválidos'}), 400
        
        admin = AdminRepository.update(id, dados)
        if admin:
            return jsonify(admin.to_dict())
        return jsonify({'erro': 'Administrador não encontrado'}), 404
    
    @staticmethod
    def delete(id):
        if AdminRepository.delete(id):
            return jsonify({'mensagem': 'Administrador deletado com sucesso'})
        return jsonify({'erro': 'Administrador não encontrado'}), 404