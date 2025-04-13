from dotenv import load_dotenv
import requests
import os

load_dotenv()

# /getUpdates
# /sendMessage?chat_id=<chat id>&text=<text>
# /sendvideo?chat_id=<chat id>&video=<video>
# -4554283755

chat_id = os.getenv("chat_id")
bot_api = os.getenv("bot_api")

video_count = 0
print("Start Bot")
while 1:
    if os.path.exists(fr".\output\bit-clip-{video_count + 1}.mp4"):
        print(f"Video Num: {video_count}")
        
        # send video with bot
        file = {"video": open(fr".\output\bit-clip-{video_count}.mp4", "rb")}
        post_requests = requests.post(f"https://api.telegram.org/bot{bot_api}/sendVideo?chat_id={chat_id}", files=file)
        print(post_requests)

        # remove the file
        os.remove(fr".\output\bit-clip-{video_count}.mp4")
        print("file removed")

        video_count = video_count + 1
        print(f"Next Video Num: {video_count}")
        print("---------------------")
