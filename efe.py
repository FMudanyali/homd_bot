from random import randint
from telegram.ext import Updater
import os
from credentials import *
from time import time

def kick_efe(bot,context):
    print("Got ban request")
    #get who issued this command
    user = context.message.from_user.id
    #get homd's admins
    admins = [admin.user.id for admin in bot.get_chat_administrators(chat_id=which_chat)]
    #check if this person is an admin
    if user in admins:
        print("User is admin")
        #select one of few ban messages
        username = context.message.from_user.first_name
        message_file = open('ban_messages.txt','r+')
        ban_messages = message_file.read().split('\n')
        message_file.close()
        ban_message=ban_messages[randint(0,len(ban_messages))]
        #select efe
        efe = bot.getChatMember(chat_id=which_chat,user_id=189748641)
        #check if efe is available
        if efe.status in ['member','restricted']:
            try:
                #kick him and unban him, so he can rejoin. Also send the ban message.
                bot.kickChatMember(chat_id=which_chat,user_id=189748641)
                bot.unbanChatMember(chat_id=which_chat,user_id=189748641)
                bot.send_message(chat_id=which_chat,text=ban_message.format(username))
                efe_tracker(bot, context)
                print("He's gone")
            except:
                return False
        else:
            #He's already gone.
            bot.send_message(chat_id=which_chat,text="The dipshit is in another castle.")
            print("He was already gone")
    else:
        #Refuse if this person is not an admin.
        print("User not admin")
        bot.send_message(chat_id=which_chat,text="You're not an admin, fuckboy.")

def efe_tracker(bot,context):
    if not os.path.exists('efe_file.txt'):
        efe_file = open('efe_file.txt','w+')
        efe_file.write(str(time()))
        efe_file.close()
    if not os.path.exists('record_file.txt'):
        record_file = open('record_file.txt','w+')
        record_file.write("0")
        record_file.close()
    
    efe = bot.getChatMember(chat_id=which_chat,user_id=189748641)
    efe_file = open('efe_file.txt', 'r')
    record_time = int(record_file.read())
    start_time = float(efe_file.read())
    efe_file.close()
    if efe.status in ['member','restricted']:
        elapsed_time = time() - start_time
        hour = int(elapsed_time // 3600)
        minute = int(elapsed_time % 3600 // 60)
        if hour == 0: fm_hour=""
        else: fm_hour = f"{hour} hours and " if hour>1 else "an hour and "
        fm_minute = f"{minute} minutes" if minute>1 else "a minute"
        bot.send_message(chat_id=which_chat,text=f"Efe hasn't been kicked for {fm_hour}{fm_minute}.")
    else:
        if elapsed_time > record_time:
            record_time = elapsed_time
            record_file = open('record_file.txt','w')
            record_file.write(record_time)
            record_file.close()
        rc_hour = int(record_time // 3600)
        rc_minute = int(record_time % 3600 // 60)
        if rc_hour == 0: fmrc_hour=""
        else: fmrc_hour = f"{hour} hours and " if rc_hour>1 else "an hour and "
        fmrc_minute = f"{rc_minute} minutes" if rc_minute>1 else "a minute"
        os.system("rm efe_file.txt")
        bot.send_message(chat_id=which_chat,text=f"Efe is gone. His record time is {fmrc_hour}{fmrc_minute}.")
        efe_file = open('efe_file.txt','w+')
        efe_file.write(str(time()))
        efe_file.close()