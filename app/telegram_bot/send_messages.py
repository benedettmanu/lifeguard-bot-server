# lifeguard-bot-server/telegram_bot/send_messages.py
from app.models.usuario import Usuario
from app import db
from .bot import bot

# Função para enviar mensagem para números específicos cadastrados em um CEP


def enviar_mensagem_para_cep(cep, mensagem):
    numeros_cadastrados = obter_numeros_por_cep(cep)
    for numero in numeros_cadastrados:
        enviar_mensagem(numero, mensagem)


def enviar_mensagem(chat_id, mensagem):
    bot.send_message(chat_id, mensagem)


def obter_numeros_por_cep(cep):
    try:
        # Consulta os usuários cadastrados no banco de dados pelo CEP
        usuario = Usuario.query.filter_by(cep=cep).all()
        # Filtra telefones não nulos
        numeros = [usuario.telefone for usuario in usuario if usuario.telefone]
        return numeros
    except Exception as e:
        print(f'Erro ao obter números por CEP {cep}: {e}')
        return []
