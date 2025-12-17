import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ========================
# VARIÁVEIS
# ========================
users = {}
WAITING_CAPS = 1

# ========================
# FUNÇÕES AUXILIARES
# ========================
def contador_msg(user_id):
    users[user_id] = users.get(user_id, 0) + 1
    return users[user_id]

# ========================
# COMANDOS
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "E aí, meu consagrado! 😎\n"
        "Eu sou o bot do Darth!\n"
        "Manda qualquer coisa que eu repito pra você!"
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Comandos:\n"
        "/start\n"
        "/help\n"
        "/caps\n"
        "/menu\n"
        "/info\n\n"
        "Mensagens normais → eco com contador 😎"
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot do Darth\n"
        "Criado por Darth 🚀\n"
        "Versão 1.0"
    )

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Manda o texto depois do comando!\n"
            "Exemplo: /caps bora lá"
        )
    else:
        contador_msg(update.effective_user.id)
        texto = " ".join(context.args).upper()
        await update.message.reply_text(f"{texto} 🔥")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contador_msg(update.effective_user.id)
    count = users.get(update.effective_user.id, 0)
    await update.message.reply_text(
        f"Você disse: {update.message.text}\n"
        f"Essa é sua {count}ª mensagem 😜"
    )

# ========================
# MENU INLINE
# ========================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Maiúsculo", callback_data="caps"),
            InlineKeyboardButton("Contador", callback_data="contador")
        ],
        [
            InlineKeyboardButton("Site do Guanabara", url="https://cursoemvideo.com"),
            InlineKeyboardButton("Fechar menu", callback_data="fechar")
        ]
    ])
    await update.message.reply_text("📋 Menu do Bot Darth:", reply_markup=keyboard)

# ========================
# CONVERSATION (CAPS)
# ========================
async def caps_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Manda o texto que quer em MAIÚSCULO! 🚀")
    return WAITING_CAPS

async def receive_caps_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text
