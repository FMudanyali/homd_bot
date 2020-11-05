from random import randint
from telegram.ext import Updater
import os,logging
from credentials import *
import telegram.ext
from time import time
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def kick_efe(update, context):
    #get who issued this command
    user = update.message.from_user.id
    #get homd's admins
    admins = [admin.user.id for admin in context.bot.get_chat_administrators(chat_id=which_chat)]
    #check if this person is an admin
    if user in admins:
        #select one of few ban messages
        username = update.message.from_user.first_name
        message_file = open('ban_messages.txt','r+')
        ban_messages = message_file.read().split('\n')
        message_file.close()
        ban_message=ban_messages[randint(0,len(ban_messages)-1)]
        #select efe
        efe = context.bot.getChatMember(chat_id=which_chat,user_id=189748641)
        #check if efe is available
        if efe.status in ['member','restricted']:
            try:
                #kick him and unban him, so he can rejoin. Also send the ban message.
                context.bot.kickChatMember(chat_id=which_chat,user_id=189748641)
                context.bot.unbanChatMember(chat_id=which_chat,user_id=189748641)
                context.bot.send_message(chat_id=which_chat,text=ban_message.format(username))
                efe_tracker(update, context)
            except:
                return False
        else:
            #He's already gone.
            context.bot.send_message(chat_id=which_chat,text="The dipshit is in another castle.")
    else:
        #Refuse if this person is not an admin.
        context.bot.send_message(chat_id=which_chat,text="You're not an admin, fuckboy.")



def efe_record(update, context):
    efe = context.bot.getChatMember(chat_id=which_chat,user_id=189748641)
    record_file = open('record_file.txt', 'r')
    record_time = float(record_file.read())
    record_file.close()
    rc_hour = int(record_time // 3600)
    rc_minute = int(record_time % 3600 // 60)
    if rc_hour == 0: fmrc_hour=""
    else: fmrc_hour = f"{rc_hour} hours and " if rc_hour>1 else "an hour and "
    fmrc_minute = f"{rc_minute} minutes" if rc_minute>1 else "a minute"
    context.bot.send_message(chat_id=which_chat,text=f"His record time is {fmrc_hour}{fmrc_minute}.")

def efe_info(context: telegram.ext.CallbackContext):
    if not os.path.exists('efe_file.txt'):
        efe_file = open('efe_file.txt','w+')
        efe_file.write(str(time()))
        efe_file.close()
    if not os.path.exists('record_file.txt'):
        record_file = open('record_file.txt','w+')
        record_file.write("0")
        record_file.close()
    efe = context.bot.getChatMember(chat_id=which_chat,user_id=189748641)
    efe_file = open('efe_file.txt', 'r')
    record_file = open('record_file.txt', 'r')
    record_time = float(record_file.read())
    start_time = float(efe_file.read())
    efe_file.close()
    record_file.close()

    if efe.status in ['member','restricted']:
        elapsed_time = time() - start_time
        hour = int(elapsed_time // 3600)
        minute = int(elapsed_time % 3600 // 60)
        if hour == 0: fm_hour=""
        else: fm_hour = f"{hour} hours and " if hour>1 else "an hour and "
        fm_minute = f"{minute} minutes" if minute>1 else "a minute"
        return True,fm_hour,fm_minute
    else:
        elapsed_time = time() - start_time
        if elapsed_time > record_time:
            record_time = elapsed_time
            record_file = open('record_file.txt','w')
            record_file.write(str(record_time))
            record_file.close()
        rc_hour = int(record_time // 3600)
        rc_minute = int(record_time % 3600 // 60)
        if rc_hour == 0: fmrc_hour=""
        else: fmrc_hour = f"{rc_hour} hours and " if rc_hour>1 else "an hour and "
        fmrc_minute = f"{rc_minute} minutes" if rc_minute>1 else "a minute"
        os.system("rm efe_file.txt")
        efe_file = open('efe_file.txt','w+')
        efe_file.write(str(time()))
        efe_file.close()
        return False,fmrc_hour,fmrc_minute

def efe_tracker(update, context):
    status,hour,minute = efe_info(context)
    if status:
        context.bot.send_message(chat_id=which_chat,text=f"Efe hasn't been kicked for {hour}{minute}.")
    else:
        context.bot.send_message(chat_id=which_chat,text=f"Efe is gone. His record time is {hour}{minute}.")