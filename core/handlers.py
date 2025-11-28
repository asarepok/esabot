from telegram.ext import CommandHandler
import callbacks

HANDLERS = [
    CommandHandler('start', callbacks.start)
]