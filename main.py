import logging
from telegram import Update
from telegram.ext import ApplicationBuilder

from dotenv import load_dotenv
import os

from core.handlers import HANDLERS

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
load_dotenv(override=True)


def main():
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    application.add_handlers(HANDLERS)

    if os.getenv("WEBHOOK_HOST") is not None and os.getenv("WEBHOOK_PORT") is not None and os.getenv("WEBHOOK_SECRET") is not None and os.getenv("WEBHOOK_URL") is not None:
        application.run_webhook(
            listen=os.getenv("WEBHOOK_HOST"),
            port=int(os.getenv("WEBHOOK_PORT")),
            secret_token=os.getenv("WEBHOOK_SECRET"),
            webhook_url=os.getenv("WEBHOOK_URL")
        )
    else:
        application.run_polling()


if __name__ == "__main__":
    main()