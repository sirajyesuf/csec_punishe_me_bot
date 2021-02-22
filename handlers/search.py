from telegram import Update,ReplyKeyboardMarkup, chat
from telegram.ext import (

    MessageHandler,
    ConversationHandler,
    Filters, conversationhandler, filters
)
from telegram.ext.callbackcontext import CallbackContext
from api import search_user
from .start import home_kbd

INPUT_NAME_MEMEBER = range(1)



def search(update:Update,context:CallbackContext)->int:
    context.bot.send_message(
        chat_id = update.effective_user.id,
        text = "🔍 🔎hi i am here to help you to verify the membership of the person just enter his/her name",
        reply_markup = ReplyKeyboardMarkup([
            ['Cancel']
        ],resize_keyboard = True)

    )

    return INPUT_NAME_MEMEBER

def get_input_from_user(update:Update,context:CallbackContext)->int:
    key = update.message.text
    if search_user(key_word=key)['data']:
        context.bot.send_message(
            chat_id = update.effective_user.id,
            text = "✅ {} found|200".format(key)
        )
    else:
        context.bot.send_message(
            chat_id = update.effective_user.id,
            text = "❌{} not found |404".format(key)

        )
        context.bot.send_message(
            chat_id = update.effective_user.id,
            text = "enter another"
        )
    return INPUT_NAME_MEMEBER


def cancel(update,context):
    context.bot.send_message(
        chat_id = update.effective_user.id,
        text = "canceled",
        reply_markup = home_kbd
    )
    return conversationhandler.End



































btn = ['🔍Search']
search_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(btn),search)],
    states={
        INPUT_NAME_MEMEBER:[
            MessageHandler(Filters.text & ~(Filters.text(btn)),get_input_from_user)

        ]

    },
    fallbacks=[
        MessageHandler(Filters.text & ~(Filters.text(btn)),cancel)
    ]
)