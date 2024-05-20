from flask import Blueprint, jsonify, request
from app import db
from app.models.usuario import Usuario
import flask_login

usuario_routes = Blueprint('usuario_routes', __name__)

@usuario_routes.route('/criaLogin', methods=['POST'])
def criaLogin():
    data = request.get_json()
    novo_usuario = Usuario(**data)
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201


@usuario_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data['email']).first()
    if usuario and usuario.senha == data['senha']:
        flask_login.login_user(usuario)
        user_data = {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'telefone': usuario.telefone,
            'cep': usuario.cep,
            'logradouro': usuario.logradouro,
            'bairro': usuario.bairro,
            'cidade': usuario.cidade,
            'autoridade': usuario.is_authority,
            'adm': usuario.is_adm
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'Erro: Email ou senha inválidos!'}), 401


@usuario_routes.route("/listaUsuario")
def listaUsuario():
    usuarios = Usuario.query.all()
    return jsonify([{'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email, 'telefone': usuario.telefone, 'cep': usuario.cep, 'logradouro': usuario.logradouro, 'cidade': usuario.cidade, 'bairro': usuario.bairro, 'autoridade': usuario.is_authority, 'adm': usuario.is_adm} for usuario in usuarios])
