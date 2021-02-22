from functools import wraps
from api import get_user_info

def only_decipline_commite(func):
    def wrapper(update,context,*args,**kwargs):
        if(get_user_info(update.effective_user.id)):
            func(update,context,*args,**kwargs)
        else:
            context.bot.send_message(
                chat_id = update.effective_user.id,
                text = "no {}".format(update.effective_user.id)
            )
    return wrapper

