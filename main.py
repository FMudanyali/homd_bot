import os,pickle
from credentials import *
from tweepy import OAuthHandler,API,Cursor
from time import sleep
from random import randint
from telegram.ext import Updater,CommandHandler

def kick_efe(bot,context):
    #get who issued this command
    user = context.message.from_user.id
    #get homd's admins
    admins = [admin.user.id for admin in bot.get_chat_administrators(chat_id=which_chat)]
    #check if this person is an admin
    if user in admins:
        #select one of few ban messages
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
                bot.send_message(chat_id=which_chat,text=ban_message)
            except:
                return False
        else:
            #He's already gone.
            bot.send_message(chat_id=which_chat,text="The dipshit is in another castle.")
    else:
        #Refuse if this person is not an admin.
        bot.send_message(chat_id=which_chat,text="You're not an admin, fuckboy.")

def call_memes(bot,context):
    global access_key,access_key_secret,consumer_key,consumer_key_secret
    #initialize twitter
    auth = OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_key, access_key_secret)
    api = API(auth)
    #call the meme downloading function
    download_memes(bot,api,'track.txt','pages.txt',which_chat)

    print("Made a meme check.")

def download_memes(bot,api,track_txt,pages_txt,which_chat):
    #create files if they don't exist
    if not os.path.exists(track_txt):
        track_file = open(track_txt,'w+')
        track_file.close()

    if not os.path.exists(pages_txt):
        pages_file = open(pages_txt,'w+')
        pages_file.close()

    if not os.path.exists('video.pckl'):
        videos_file = open('videos.pckl', 'wb+')
        videos = 0
        pickle.dump(videos, videos_file)
        videos_file.close()
    #open files and track them into lists, variable in pickle's case
    track_file = open(track_txt,'r+')
    pages_file = open(pages_txt,'r+')
    videos_file = open('videos.pckl', 'rb+')
    videos = pickle.load(videos_file)
    track = track_file.read().split('\n')
    pages = pages_file.read().split('\n')
    videos_file.close()
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
                try:
                    os.system(f"youtube-dl -o 'videos/{tweet.id}.mp4' 'https://twitter.com/{user}/status/{tweet.id}'")
                except:
                    continue
                print(f"sending {tweet.id} from {user}")
                #try sending it to telegram chat
                try:
                     bot.send_video(chat_id=which_chat,video=open(f"videos/{tweet.id}.mp4", 'rb'), supports_streaming=True, timeout=10000)
                except:
                    continue
                #remove the video since its not needed anymore
                print(f"removing {tweet.id} from {user}")
                if os.path.exists(f"videos/{tweet.id}.mp4"): videos += 1
                os.system(f"rm videos/{tweet.id}.mp4")
    videos_file=open('videos.pckl', 'wb')
    pickle.dump(videos, videos_file)
    videos_file.close()

def videos_sent(bot,context):
    global which_chat
    #read the track file
    videos_file = open('videos.pckl', 'rb+')
    videos = pickle.load(videos_file)
    videos_file.close()
    #get user name
    user = context.message.from_user.first_name
    bot.send_message(chat_id=which_chat,text=f"{videos} videos has been sent so far, {user}.")

def main():
    global bot_token,which_chat
    #initialize bot
    bot_updater = Updater(token=bot_token)
    dispatcher = bot_updater.dispatcher
    #add commands to listen to and their respectful functions
    dispatcher.add_handler(CommandHandler('banefe',kick_efe))
    dispatcher.add_handler(CommandHandler('memeinfo',videos_sent))
    #set the job
    j = bot_updater.job_queue
    memes = j.run_repeating(call_memes, interval=900, first=0)
    #listen to commands
    bot_updater.start_polling()
    bot_updater.idle()

if __name__ == '__main__': main()
