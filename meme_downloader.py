from tweepy import OAuthHandler,API,Cursor
from credentials import *
import os

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

    if not os.path.exists('videotrack.txt'):
        videos_file = open('videotrack.txt', 'w')
        videos = 0
        videos_file.write(str(videos))
        videos_file.close()
    #open files and track them into lists, variable in video track's case
    track_file = open(track_txt,'r+')
    pages_file = open(pages_txt,'r+')
    videos_file = open('videotrack.txt', 'r')
    videos = int(videos_file.read())
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
    videos_file=open('videotrack.txt', 'w')
    videos_file.write(str(videos))
    videos_file.close()