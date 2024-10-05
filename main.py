from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

import os
import inspect
import functionalities as func

load_dotenv()
TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN')
BOT_USERNAME=os.getenv('BOT_USERNAME')
FEATURES = inspect.getmembers(func, inspect.isfunction)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


def main():
    print("Starting bot ...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    for F in FEATURES:
        name = F[0].split("_")
        function = F[1]
        match name[1]:
            case "command":
                app.add_handler(CommandHandler(name[0], function))
                print(name)
            case "messageTEXT":
                app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, function))
                print(name)
                
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval= 3)


if __name__ == '__main__':
    main()

