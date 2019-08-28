import os,telegram
from credentials import *
from tweepy import OAuthHandler,API,Cursor
from time import sleep


def start(bot,api,track_txt,pages_txt,which_chat):

    track_file = open(track_txt,'w+')
    pages_file = open(pages_txt,'r+')

    track = track_file.readlines()
    pages = pages_file.readlines()

    for user in pages:
        new_tweets = api.user_timeline(screen_name = user,count=10)
        for tweet in new_tweets:
            if tweet not in track:
                track.append(tweet.id)
                track_file.write(f"{tweet.id}\n")
                print(f"downloading {tweet.id}")
                os.system(f"/usr/bin/youtube-dl -i -o 'videos/{tweet.id}.mp4' 'https://twitter.com/{user}/status/{tweet.id}'")
                print(f"sending {tweet.id}")
                try:
                    bot.send_video(chat_id=which_chat,video=open(f"videos/{tweet.id}.mp4", 'rb'), supports_streaming=True, timeout=10000)
                except:
                    continue
                print(f"removing {tweet.id}")
                os.system(f"rm videos/{tweet.id}.mp4")

    track_file.close()
    pages_file.close()

def main():
    global bot_token,access_key,access_key_secret,consumer_key,consumer_key_secret,which_chat
    #initialize bot
    bot = telegram.Bot(bot_token)
    #initialize twitter
    auth = OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_key, access_key_secret)
    api = API(auth)
    #run the code
    while True:
        start(bot,api,'track.txt','pages.txt',which_chat)
        sleep(1800)

if __name__ == '__main__': main()
