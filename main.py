from telegram.ext import Updater,CommandHandler
from efe import *
from meme_downloader import *

def videos_sent(update, context):
    global which_chat
    #read the track file
    print("Got track request.")
    videos_file = open('videotrack.txt', 'r')
    videos = videos_file.read()
    print(f"It's {videos}")
    videos_file.close()
    #get user name
    user = update.message.from_user.first_name
    context.bot.send_message(chat_id=which_chat,text=f"{videos} videos have been sent so far, {user}.")
    print("Sent track request.")

def main():
    global bot_token,which_chat
    #initialize bot
    bot_updater = Updater(token=bot_token)
    dispatcher = bot_updater.dispatcher
    #add commands to listen to and their respectful functions
    dispatcher.add_handler(CommandHandler('banefe',kick_efe))
    dispatcher.add_handler(CommandHandler('efeinfo',efe_tracker))
    dispatcher.add_handler(CommandHandler('eferecord',efe_record))
    dispatcher.add_handler(CommandHandler('memeinfo',videos_sent))
    #set the job
    j = bot_updater.job_queue
    j.run_repeating(call_memes, interval=1800, first=0)
    j.run_repeating(efe_info, interval=60, first=0)
    #listen to commands
    bot_updater.start_polling()
    bot_updater.idle()

if __name__ == '__main__': main()
