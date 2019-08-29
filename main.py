import os,telegram
from credentials import *
from tweepy import OAuthHandler,API,Cursor
from time import sleep
from random import randint
from telegram.ext import Updater,CommandHandler

def kick_efe(bot,context):
    user = context.message.from_user.id
    admins = [admin.user.id for admin in bot.get_chat_administrators(chat_id=which_chat)]
    if user in admins:
        message_file = open('ban_messages.txt','r+')
        ban_messages = message_file.read().split('\n')
        message_file.close()
        ban_message=ban_messages[randint(0,len(ban_messages))]
        efe = bot.getChatMember(chat_id=which_chat,user_id=189748641)
        if efe.status in ['member','restricted']:
            try:
                bot.kickChatMember(chat_id=which_chat,user_id=189748641)
                bot.unbanChatMember(chat_id=which_chat,user_id=189748641)
                bot.send_message(chat_id=which_chat,text=ban_message)
            except:
                return False
        else:
            bot.send_message(chat_id=which_chat,text="The dipshit is in another castle.")
    else:
        bot.send_message(chat_id=which_chat,text="You're not an admin, fuckboy.")

def call(bot,context):
    global access_key,access_key_secret,consumer_key,consumer_key_secret

    auth = OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_key, access_key_secret)
    api = API(auth)

    start(bot,api,'track.txt','pages.txt',which_chat)
    print("Made a meme check.")

def start(bot,api,track_txt,pages_txt,which_chat):
    #open files and parse them into lists
    track_file = open(track_txt,'r+')
    pages_file = open(pages_txt,'r')
    track = track_file.read().split('\n')
    pages = pages_file.read().split('\n')
    track_file.close()
    pages_file.close()
    #for each user in pages list
    for user in pages:
        #get first 10 tweets
        new_tweets = api.user_timeline(screen_name = user,count=30)
        #for each tweet if these tweets are not in the track list
        for tweet in new_tweets:
            if str(tweet.id) not in track:
                #add this tweet id to track list so it wont get sent next time
                track.append(tweet.id)
                track_file = open(track_txt,'a')
                track_file.write(f"{tweet.id}\n")
                track_file.close()
                #download via youtube-dl
                print(f"downloading {tweet.id} from {user}")
                os.system(f"youtube-dl -i -o 'videos/{tweet.id}.mp4' 'https://twitter.com/{user}/status/{tweet.id}'")
                print(f"sending {tweet.id} from {user}")
                #try sending it to telegram chat
                try:
                    bot.send_video(chat_id=which_chat,video=open(f"videos/{tweet.id}.mp4", 'rb'), supports_streaming=True, timeout=10000)
                except:
                    continue
                #remove the video since its not needed anymore
                print(f"removing {tweet.id} from {user}")
                os.system(f"rm videos/{tweet.id}.mp4")

def main():
    global bot_token,which_chat
    #initialize bot
    bot = telegram.Bot(bot_token)

    bot_updater = Updater(token=bot_token)
    dispatcher = bot_updater.dispatcher
    dispatcher.add_handler(CommandHandler('banefe',kick_efe))
    
    #initialize twitter
    #run the code
    j = bot_updater.job_queue
    memes = j.run_repeating(call, interval=900, first=0)
    bot_updater.start_polling()
    bot_updater.idle()

if __name__ == '__main__': main()
