import os
from dotenv import load_dotenv
from telegram.update import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
import llm_rag

# Load environment variables from .env file
load_dotenv()

# Telegram bot token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(f"Hi {user.mention_markdown_v2()}")


# Message handler
def respond(update: Update, context: CallbackContext) -> None:
    """Respond to user messages with the assistant's response."""
    user_input = update.message.text
    if user_input in ("update"):
        llm_rag.update_data()
    response = llm_rag.rag_assistant.print_response(user_input)
    update.message.reply_text(response)


def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == "__main__":
    main()
