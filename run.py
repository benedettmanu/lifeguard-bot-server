from app import create_app, db
from app.routes.usuario_routes import usuario_routes
from app.routes.area_alagada_routes import area_alagada_routes
from app.telegram_bot.bot import bot


app = create_app()

app.register_blueprint(usuario_routes)
app.register_blueprint(area_alagada_routes)


if __name__ == '__main__':
    bot.infinity_polling()
    app.run(debug=True)
