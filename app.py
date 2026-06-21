from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
from functools import wraps

app = Flask(__name__, template_folder='views', static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@127.0.0.1/desenvolvimento_web"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-mude-para-uma-mais-segura'

db = SQLAlchemy(app)

# ==================== MODELOS ====================

class Problema(db.Model):
    __tablename__ = 'problemas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    dados = db.Column(db.Text)
    resultado = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'dados': self.dados,
            'resultado': self.resultado,
            'data_criacao': self.data_criacao.strftime('%Y-%m-%d %H:%M:%S') if self.data_criacao else None
        }

class Admin(db.Model):
    __tablename__ = 'administradores'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'data_cadastro': self.data_cadastro.strftime('%Y-%m-%d %H:%M:%S') if self.data_cadastro else None
        }

# ==================== REPOSITORIES ====================

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
    def login(email, senha):
        return Admin.query.filter_by(email=email, senha=senha).first()
    
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

# ==================== FUNÇÃO DE AUTENTICAÇÃO ====================

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'erro': 'Token não fornecido'}), 401
        
        try:
            token = token.split(' ')[1]
            dados = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            usuario = Admin.query.get(dados['id'])
            if not usuario:
                return jsonify({'erro': 'Usuário não encontrado'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    return decorated

# ==================== ROTAS WEB ====================

@app.route('/')
def index():
    enunciado = "DESENVOLVIMENTO WEB II - Unidade 1 - Tarefa MVC"
    return render_template('index/index.html', enunciado=enunciado)


@app.route('/frontend')
def frontend():
    return render_template('frontend.html')


@app.route('/problema', methods=['GET', 'POST'])
def problema():
    if request.method == 'POST':
        dados = request.form.get('dados')
        if dados:
            novo_problema = Problema(
                titulo="Problema Exemplo",
                descricao="Descrição do problema",
                dados=dados,
                resultado=f"Dados processados: {dados}"
            )
            ProblemaRepository.add(novo_problema)
            return render_template('problema/problema.html',
                                 enunciado="Problema de Exemplo",
                                 resultado=f"Dados processados: {dados}",
                                 dados_recebidos=dados)
    return render_template('problema/problema.html',
                         enunciado="Problema de Exemplo",
                         resultado="Nenhum dado processado",
                         dados_recebidos=None)

@app.route('/autor')
def autor():
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

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# ==================== ENDPOINT DE LOGIN ====================

@app.route('/api/login', methods=['POST'])
def login():
    dados = request.get_json()
    
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    email = dados.get('email')
    senha = dados.get('senha')
    
    if not email or not senha:
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
    
    admin = AdminRepository.login(email, senha)
    
    if not admin:
        return jsonify({'erro': 'Email ou senha inválidos'}), 401
    
    token = jwt.encode({
        'id': admin.id,
        'email': admin.email,
        'nome': admin.nome,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'usuario': admin.to_dict()
    }), 200

# ==================== ENDPOINTS RESTful - PROBLEMAS ====================

@app.route('/api/problemas', methods=['GET'])
def api_problemas_get_all():
    problemas = ProblemaRepository.get_all()
    return jsonify([p.to_dict() for p in problemas])

@app.route('/api/problemas/<int:id>', methods=['GET'])
def api_problemas_get_by_id(id):
    problema = ProblemaRepository.get_by_id(id)
    if problema:
        return jsonify(problema.to_dict())
    return jsonify({'erro': 'Problema não encontrado'}), 404

@app.route('/api/problemas', methods=['POST'])
@token_required
def api_problemas_create():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    problema = Problema(
        titulo=dados.get('titulo', ''),
        descricao=dados.get('descricao', ''),
        dados=dados.get('dados', ''),
        resultado=dados.get('resultado', '')
    )
    ProblemaRepository.add(problema)
    return jsonify(problema.to_dict()), 201

@app.route('/api/problemas/<int:id>', methods=['PUT'])
@token_required
def api_problemas_update(id):
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    problema = ProblemaRepository.update(id, dados)
    if problema:
        return jsonify(problema.to_dict())
    return jsonify({'erro': 'Problema não encontrado'}), 404

@app.route('/api/problemas/<int:id>', methods=['DELETE'])
@token_required
def api_problemas_delete(id):
    if ProblemaRepository.delete(id):
        return jsonify({'mensagem': 'Problema deletado com sucesso'})
    return jsonify({'erro': 'Problema não encontrado'}), 404

# ==================== ENDPOINTS RESTful - ADMINISTRADORES ====================

@app.route('/api/admins', methods=['GET'])
def api_admins_get_all():
    admins = AdminRepository.get_all()
    return jsonify([a.to_dict() for a in admins])

@app.route('/api/admins/<int:id>', methods=['GET'])
def api_admins_get_by_id(id):
    admin = AdminRepository.get_by_id(id)
    if admin:
        return jsonify(admin.to_dict())
    return jsonify({'erro': 'Administrador não encontrado'}), 404

@app.route('/api/admins', methods=['POST'])
def api_admins_create():
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

@app.route('/api/admins/<int:id>', methods=['PUT'])
@token_required
def api_admins_update(id):
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400
    
    admin = AdminRepository.update(id, dados)
    if admin:
        return jsonify(admin.to_dict())
    return jsonify({'erro': 'Administrador não encontrado'}), 404

@app.route('/api/admins/<int:id>', methods=['DELETE'])
@token_required
def api_admins_delete(id):
    if AdminRepository.delete(id):
        return jsonify({'mensagem': 'Administrador deletado com sucesso'})
    return jsonify({'erro': 'Administrador não encontrado'}), 404

# ==================== CRIAÇÃO DAS TABELAS ====================

with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)