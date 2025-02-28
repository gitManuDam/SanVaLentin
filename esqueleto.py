from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from diccionarioAUtilizar import personas

TOKEN = "8039630824:AAGZb3MNLbxqCYp0Jf6bp4JkFv1ZjVrQwos"
PREGUNTAS = {
    "Sexo": ["Hombre", "Mujer"],
    "Grado": ["Informatica", "Deporte", "Mecanizado", "Comercio"],
    "Fin": ["Nada serio", "Duda", "Relacion estable"],
    "Hijos": ["No quiere", "Duda", "Si quiere"]
}

historico = []


def obtener_teclado(opciones):
    return ReplyKeyboardMarkup([[opcion] for opcion in opciones], resize_keyboard=True, one_time_keyboard=True)


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        f"¡Hola, {update.effective_user.first_name}! 😊\nUsa /love para comenzar el cuestionario.")


async def stop(update: Update, context: CallbackContext) -> None:
    if historico:
        historico.clear()
        await update.message.reply_text("Cuestionario cancelado. Escribe /love para volver a empezar.")
    else:
        await update.message.reply_text("No hay un cuestionario en marcha. Escribe /love para empezar.")


async def back(update: Update, context: CallbackContext) -> None:
    if historico:
        historico.pop()
        await update.message.reply_text("Última respuesta eliminada. Vuelve a contestarla.")
    else:
        await update.message.reply_text("No hay respuestas para borrar. Escribe /love para comenzar.")


async def love(update: Update, context: CallbackContext) -> None:
    if historico:
        await update.message.reply_text("Ya hay un cuestionario en marcha.")
    else:
        historico.append("Empezar")
        await update.message.reply_text("Escribe tu nombre completo:")


async def option_selected(update: Update, context: CallbackContext) -> None:
    mensaje = update.message.text
    pasos = len(historico)

    if pasos == 1:
        historico.append(mensaje)
        await update.message.reply_text("Introduce tu edad:")
    elif pasos == 2:
        if mensaje.isdigit():
            historico.append(mensaje)
            await update.message.reply_text("Introduce tu sexo:", reply_markup=obtener_teclado(PREGUNTAS["Sexo"]))
        else:
            await update.message.reply_text("Introduce una edad válida:")
    elif pasos == 3 and mensaje in PREGUNTAS["Sexo"]:
        historico.append(mensaje)
        await update.message.reply_text("Introduce tu grado:", reply_markup=obtener_teclado(PREGUNTAS["Grado"]))
    elif pasos == 4 and mensaje in PREGUNTAS["Grado"]:
        historico.append(mensaje)
        await update.message.reply_text("Introduce tu finalidad:", reply_markup=obtener_teclado(PREGUNTAS["Fin"]))
    elif pasos == 5 and mensaje in PREGUNTAS["Fin"]:
        historico.append(mensaje)
        await update.message.reply_text("Introduce si quieres hijos:", reply_markup=obtener_teclado(PREGUNTAS["Hijos"]))
    elif pasos == 6 and mensaje in PREGUNTAS["Hijos"]:
        historico.append(mensaje)
        mensaje_final = buscar_personas_afines(historico)
        historico.clear()
        await update.message.reply_text(mensaje_final)
    else:
        await update.message.reply_text("Respuesta no válida. Inténtalo de nuevo.")


def buscar_personas_afines(datos):
    afinidades = []

    for persona in personas.values():
        afinidad = 0
        edad, sexo, grado, fin, hijos = int(datos[2]), datos[3], datos[4], datos[5], datos[6]

        if persona["Edad"] - 5 <= edad <= persona["Edad"] + 5:
            afinidad += 1
        if persona["Edad"] - 2 <= edad <= persona["Edad"] + 2:
            afinidad += 2
        if sexo != persona["Sexo"]:
            afinidad += 2
        if grado == persona["Grado"]:
            afinidad += 1
        if fin == "Duda" or persona["Fin"] == "Duda":
            afinidad += 1
        elif fin == persona["Fin"]:
            afinidad += 2
        if hijos == "Duda" or persona["Hijos"] == "Duda":
            afinidad += 1
        elif hijos == persona["Hijos"]:
            afinidad += 2

        persona["Afinidad"] = afinidad
        afinidades.append(persona)

    afinidades = sorted(afinidades, key=lambda x: x["Afinidad"], reverse=True)[:3]
    return "\n".join([
                         f"{i + 1}.- {p['NombreCompleto']} (Edad: {p['Edad']}, Sexo: {p['Sexo']}, Grado: {p['Grado']}, Fin: {p['Fin']}, Hijos: {p['Hijos']})"
                         for i, p in enumerate(afinidades)])


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("love", love))
    app.add_handler(CommandHandler("back", back))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, option_selected))
    app.run_polling()


if __name__ == "__main__":
    main()