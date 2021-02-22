
import os
import logging
from telegram.ext import Updater,PicklePersistence
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('token')


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

#handlers
from handlers.start import start_command_handler
from handlers.punishe_me import punisher_conv_handler
from handlers.search import search_conv_handler
def main():
    per = PicklePersistence(filename='persistance')
    updater = Updater(token=token,persistence=per,use_context=True)
    dispatcher = updater.dispatcher
    #add handlers
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(punisher_conv_handler)
    dispatcher.add_handler(search_conv_handler)
    
   


    
    #start the bot
    updater.start_polling()
    #until you press ctrl-c
    updater.idle()


if __name__ == '__main__':
    main()