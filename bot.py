import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes,
    CallbackQueryHandler, ConversationHandler
)

users = {}
WAITING_CAPS = 1

def contador_msg(user_id):
    users[user_id] = users.get(user_id, 0) + 1
    return users[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("E aí, meu consagrado! 😎\nEu sou o bot do Darth!\nManda qualquer coisa que eu repito pra você!")

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Manda o texto depois do comando, meu jovem! 👀\nExemplo: /caps bora lá")
    else:
        contador_msg(update.effective_user.id)
        texto = ' '.join(context.args).upper()
        await update.message.reply_text(f"{texto} 🔥")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contador_msg(update.effective_user.id)
    count = users.get(update.effective_user.id, 0)
    texto = update.message.text
    await update.message.reply_text(f"Você disse: {texto} 😜\nEssa é sua {count}ª mensagem.")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot do Darth\nCriado por Darth como aluno do Professor Guanabara 2.0 🚀\nVersão 1.0")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Comandos:\n/start\n/help\n/caps\n/menu\n/info\nMensagens normais → eco com contador 😎")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("Maiúsculo", callback_data="caps"), InlineKeyboardButton("Contador", callback_data="contador")],
        [InlineKeyboardButton("Site do Guanabara", url="https://cursoemvideo.com"), InlineKeyboardButton("Fechar menu", callback_data="fechar")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("📋 Menu do Bot Darth:", reply_markup=keyboard)

# Maiúsculo com Conversation
async def caps_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Manda o texto que quer em MAIÚSCULO! 🚀")
    return WAITING_CAPS

async def receive_caps_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    texto = update.message.text.upper()
    await update.message.reply_text(f"{texto} 🔥")
    contador_msg(update.effective_user.id)
    await update.message.reply_text("Pronto! /menu pra voltar 😎")
    return ConversationHandler.END

# Outros botões
async def other_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "contador":
        count = users.get(update.effective_user.id, 0)
        await query.edit_message_text(f"Você já mandou {count} mensagens! 📊")
    elif data == "fechar":
        await query.message.delete()

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Cancelou o maiúsculo!")
    return ConversationHandler.END

def main():
    token = os.environ["TOKEN"]
    app = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(caps_click, pattern="^caps$")],
        states={
            WAITING_CAPS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_caps_text)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("caps", caps))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(other_buttons, pattern="^(contador|fechar)$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()

if __name__ == "__main__":
    main()
