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
    efe = bot.getChatMember(chat_id=which_chat,user_id=189748641)
    start_time = time()
    if efe.status in ['member','restricted']:
        elapsed_time = time() - start_time
        hour = elapsed_time // 3600
        minute = elapsed_time % 3600 // 60
        fm_hour = f"{hour} hours" if hour>1 else "an hour"
        fm_minute = f"{minute} minutes" if minute>1 else "a minute"
        bot.send_message(chat_id=which_chat,text=f"Efe hasn't been kicked for {fm_hour} and {fm_minute}.")
    else:
        start_time = time()