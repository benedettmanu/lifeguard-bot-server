from flask import Blueprint, jsonify, request, redirect
from app import db
from app.models.usuario import Usuario
import flask_login
from flask import current_app as app

usuario_routes = Blueprint('usuario_routes', __name__)


@usuario_routes.route('/criaLogin', methods=['POST'])
def criaLogin():
    data = request.get_json()
    usuario_existente = Usuario.query.filter_by(email=data['email']).first()
    if usuario_existente:
        return jsonify({'message': 'Já existe um usuário com esse email'}), 400
    novo_usuario = Usuario(**data)
    db.session.add(novo_usuario)
    db.session.commit()

    # bot
    bot_username = 'Pedro_Salva_Vidas_bot'  # substitua pelo username do seu bot
    bot_link = f"https://t.me/{bot_username}?start={novo_usuario.id}"

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


@usuario_routes.route('/redirecionar_para_bot', methods=['GET'])
def redirecionar_para_bot():
    try:
        # Obtém o ID do usuário cadastrado no seu site
        usuario_id = request.args.get('usuario_id')

        # URL base do seu bot no Telegram
        bot_username = 'Pedro_Salva_Vidas_bot'  # substitua pelo username do seu bot
        telegram_url = f"https://t.me/{bot_username}"

        # Constrói o link de redirecionamento para o Telegram com o parâmetro start
        bot_link = f"{telegram_url}?start={usuario_id}"

        # Redireciona o usuário para o link gerado
        return redirect(bot_link)
    except Exception as e:
        # Trate qualquer exceção aqui
        return f"Erro ao redirecionar para o bot: {str(e)}"
