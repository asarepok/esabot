from telegram.ext import CommandHandler
from . import callbacks

HANDLERS = [
    CommandHandler('start', callbacks.start)
]