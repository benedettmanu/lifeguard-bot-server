from app import db, login_manager
import flask_login


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Usuario (db.Model, flask_login.UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    cep = db.Column(db.String)
    logradouro = db.Column(db.String)
    bairro = db.Column(db.String)
    cidade = db.Column(db.String)
    senha = db.Column(db.String)
    is_authority = db.Column(db.Boolean, default=False)
    is_adm = db.Column(db.Boolean, default=False)

    def __init__(self, nome, email, telefone, cep, logradouro, bairro, cidade, senha):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.cep = cep
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.senha = senha
        self.is_authority = email.endswith('@defesacivil.sc.gov.br')
        self.is_adm = email.endswith('@bot-salva-vidas.com.br')
