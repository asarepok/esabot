from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from ..locales import l


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(l("WELCOME", username=update.effective_user.name), parse_mode=ParseMode.HTML)