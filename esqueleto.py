from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from diccionarioAUtilizar import personas


TOKEN = "7676914682:AAGseR0GPhPwJZSOYC5uvGbKsFlxlEvLMco"


def main():
    """Configura y ejecuta el bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))


    app.run_polling()

if __name__ == "__main__":
    main()