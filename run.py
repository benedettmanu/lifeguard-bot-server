from app import create_app, db
from app.routes.usuario_routes import usuario_routes
from app.routes.area_alagada_routes import area_alagada_routes
from app.telegram_bot.bot import bot
from threading import Thread


app = create_app()

app.register_blueprint(usuario_routes)
app.register_blueprint(area_alagada_routes)


# bot iniciado semparado em um threand
def run_telegram_bot():
    bot.polling()


if __name__ == '__main__':
   # Iniciar o bot
    telegram_thread = Thread(target=run_telegram_bot)
    telegram_thread.start()
    app.run(debug=True)
