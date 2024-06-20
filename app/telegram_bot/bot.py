import telebot
from .send_messages import send_messages

API_TOKEN = '7239417259:AAFyNA5QS8sqFu44CPm56gsknAOPQGpkz2g'


bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Olá! Eu sou Pedro, o bot salva vidas!")



@bot.message_handler(commands=['enviar_alerta'])
def handle_enviar_alerta(message):
    try:
        cep = '88000-000'  # Substitua pelo CEP desejado
        mensagem = 'Alerta! O nível de água está alto.'
        enviar_mensagem_para_cep(cep, mensagem)
        bot.send_message(message.chat.id, f"Alerta enviado para os números cadastrados no CEP {cep}. Mensagem: {mensagem}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Erro ao enviar alerta: {str(e)}")
