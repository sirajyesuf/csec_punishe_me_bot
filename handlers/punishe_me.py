from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, chat
from telegram.ext import(
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler, conversationhandler, messagehandler,

)

from decorators import only_decipline_commite
from api import get_user_info,punishement_record,search_user
from .start import home_kbd
PUNISHER, MEMEBER_NAME, SELECT_MEMEBER,REASON = range(4)

# @only_decipline_commite


def punisher(update: Update, context: CallbackContext) -> None:
    start_punishement(update,context)
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text="🔫 pls eneter the name of the member dont forget 1 space b/n the first and the final name",
        reply_markup=ReplyKeyboardMarkup([
            ["Cancel"]
        ],resize_keyboard=True)
    )

    return MEMEBER_NAME
   

def member_name(update, context):
    full_name = update.message.text
    print(update.message.text)
    set_punishement_info(update,context,'ptelegram_user_id',update.effective_user.id)
    data = search_user(full_name)
    if data['data']:
        display_member(update, context, data=data)
        return SELECT_MEMEBER
    else:
        context.bot.send_message(
            chat_id = update.effective_user.id,
            text  = "not found|404 😔 try again",

        )
def member_pagination(update:Update,context:CallbackContext)->int:
    query = update.callback_query
    query.answer()
    data = search_user(url=query.data)
    print("message_id = ",context.user_data['message_id'])
    # query.message.delete(context.user_data['message_id'][-1])
    display_member(update, context, data=data)
    return SELECT_MEMEBER



def member_select(update:Update,context:CallbackContext)->int:
    query = update.callback_query
    query.answer()
    # query.message.delete(context.user_data['message_id'][-1])
    set_punishement_info(update,context,'ctelegram_user_id',query.data)
    context.bot.send_message(
        chat_id = update.effective_user.id,
        text = "pls enter the reason",

    )
    return REASON

def reason(update:Update,context:CallbackContext)->int:
    reason = update.message.text
    print("reason",reason)
    set_punishement_info(update,context,'reason',reason)
    context.bot.send_message(
        chat_id = update.effective_user.id,
        text = "Done"
    )
    notify_the_criminal(update,context)
    payload  = {
        'punishement':context.user_data['punishement']
    }
    punishement_record(payload)
    context.bot.send_message(
        chat_id = update.effective_user.id,
        text = "ok",
        reply_markup = home_kbd
    )
    context.user_data.clear()
    return ConversationHandler.END

def cancel(update:Update,context:CallbackContext)->int:
    context.user_data.clear()
    context.bot.send_message(
        chat_id = update.effective_user.id,
        text = "canceled",
        reply_markup = home_kbd
    )
    return ConversationHandler.END
def unknown(update,context):
    context.bot.send_message(
        chat_id = update.effective_user.id,
        text = "unknown input"
    )

btn = ['Punishe','Cancel']

punisher_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(btn), punisher)],
    states={
        MEMEBER_NAME: [
            MessageHandler(Filters.regex(r'[a-zA-Z]') & ~(Filters.text(btn)), member_name)
        ],
        SELECT_MEMEBER:[
            CallbackQueryHandler(member_pagination,pattern='^http://'),
            CallbackQueryHandler(member_select,pattern='\w')
        ],
        REASON:[
            MessageHandler(Filters.text & ~(Filters.text(btn)),reason)
        ],
        
    },
    fallbacks=[
        MessageHandler(Filters.text(btn),cancel),
        MessageHandler(Filters.all,unknown)
    ]
)


def display_member(update, context, data):
    next_url = data['links']['next']
    prev_url = data['links']['prev']
    member = data['data'][0]
    msg = "\t\t Memeber Details\t\t\n✔️full_name={}\n✔️year={}\n✔️Division={}\n✔️criminals={}".format(member['full_name'],member['year'],member['divisions'],member['criminals'])
    result = context.bot.send_message(
        chat_id = update.effective_user.id,
        text = msg,
        reply_markup = member_inline_keyboard(member['telegram_user_id'],next_url,prev_url)


    )
    context.user_data['message_id'].append(result['message_id'])





def start_punishement(update,context):
    context.user_data['punishement'] ={
        
        # 'ptelegram_user_id':
        # 'ctelegram_user_id':
        # 'reason':
    }
    context.user_data['message_id'] =[]
def set_punishement_info(update,context,key,value):
    context.user_data['punishement'][key] = value
    print(context.user_data['punishement'])

def notify_the_criminal(update,context):
    reason =context.user_data['punishement']['reason']
    msg = "👋 You have a message from Displice commite @{}  \n\n 📜you charge is ={}".format(update.message.from_user.username,reason)
    print(update)
    context.bot.send_message(
        chat_id = int(context.user_data['punishement']['ctelegram_user_id']),
        text = msg
    )
















from telegram import InlineKeyboardButton,InlineKeyboardMarkup

def member_inline_keyboard(user_id,next_url=None,prev_url=None):
    keyboard =[]
    if(next_url and not prev_url):
        keyboard.append(InlineKeyboardButton(text="⏭️next",callback_data=next_url))
        keyboard.append(InlineKeyboardButton(text="❤️select",callback_data=user_id))

    if(prev_url and not next_url):
        keyboard.append(InlineKeyboardButton(text="⏮️prev",callback_data=prev_url))
        keyboard.append(InlineKeyboardButton(text="❤️select",callback_data=user_id))
    if(next_url and prev_url):
        keyboard.append(InlineKeyboardButton(text="⏭️next",callback_data=next_url))
        keyboard.append(InlineKeyboardButton(text="❤️select",callback_data=user_id))
        keyboard.append(InlineKeyboardButton(text="⏮️prev",callback_data=prev_url))
    if(not next_url and not prev_url):
        keyboard.append(InlineKeyboardButton(text="❤️select",callback_data=user_id))
    return InlineKeyboardMarkup([keyboard])    










