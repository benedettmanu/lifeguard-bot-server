import telebot

# Insira aqui o token do seu bot
API_TOKEN = '7239417259:AAFyNA5QS8sqFu44CPm56gsknAOPQGpkz2g'


# Criação do objeto bot
bot = telebot.TeleBot(API_TOKEN)

# Exemplo de função no bot para enviar mensagem


def enviar_mensagem(chat_id, mensagem):
    bot.send_message(chat_id, mensagem)

# Exemplo de resposta a uma mensagem recebida


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(message, "Olá! Este é um teste.")

# Não inicia o polling aqui, pois será iniciado no script principal (run.py)
