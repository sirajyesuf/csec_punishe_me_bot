
from telegram import Update
from telegram.ext import CallbackContext,CommandHandler
from decorators import only_decipline_commite
from telegram import ReplyKeyboardMarkup



home_kbd = ReplyKeyboardMarkup([

            ['Punishe','🔍Search']
        ],resize_keyboard=True)

   

@only_decipline_commite
def start(update:Update,context:CallbackContext)->None:
    context.bot.send_message(
        chat_id = update.effective_user.id,
        text = "welcome",
        reply_markup = home_kbd
    )


start_command_handler = CommandHandler('start',start)




