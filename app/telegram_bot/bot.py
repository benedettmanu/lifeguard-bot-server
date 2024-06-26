from app import db
from app.models.usuario import Usuario
import telebot


API_TOKEN = '7239417259:AAFyNA5QS8sqFu44CPm56gsknAOPQGpkz2g'


bot = telebot.TeleBot(API_TOKEN)


# Função para enviar mensagem para números específicos cadastrados em um CEP
def enviar_mensagem_para_cep(cep, mensagem):
    usuarios_cadastrados = obter_usuarios_por_cep(cep)
    for usuario in usuarios_cadastrados:
        enviar_mensagem(usuario.chat_id, mensagem)


def enviar_mensagem(chat_id, mensagem):
    bot.send_message(chat_id, mensagem)


def obter_usuarios_por_cep(cep):
    try:
        # Consulta os usuários cadastrados no banco de dados pelo CEP
        usuarios = Usuario.query.filter_by(cep=cep).all()
        return usuarios
    except Exception as e:
        print(f'Erro ao obter usuários por CEP {cep}: {e}')
        return []


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        usuario = Usuario.query.filter_by(user_id=user_id).first()

        if usuario:
            usuario.chat_id = chat_id
            db.session.commit()
            bot.send_message(
                chat_id, "Olá! Eu sou Pedro, o bot salva vidas! Seu ID foi registrado.")
        else:
            bot.send_message(
                chat_id, "Usuário não encontrado no banco de dados. Por favor, registre-se no site.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao registrar ID: {str(e)}")


@bot.message_handler(commands=['enviar_alerta'])
def handle_enviar_alerta(message):
    try:
        cep = message.text.split()[1] if len(
            message.text.split()) > 1 else '88000-000'
        mensagem = 'Alerta! O nível de água está alto.'
        if enviar_mensagem_para_cep(cep, mensagem):
            bot.send_message(
                message.chat.id, "Alerta enviado para os números cadastrados no CEP {cep}. Mensagem: {mensagem}")

        else:
            bot.send_message(
                message.chat.id, f"Erro ao enviar alerta para o CEP {cep}.")
    except IndexError:
        bot.send_message(
            message.chat.id, "Por favor, forneça um CEP válido após o comando /enviar_alerta.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao enviar alerta: {str(e)}")


# Inicie o bot
bot.polling()
