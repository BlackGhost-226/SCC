import database
import random
from scc import SCC


duration_video = 15
words_in_line = 3
videoCount = -1
url_font = None
text_p = 1900

url_backgroundVideo_in = None
url_img_in = None
url_audio_in = None
texts_in = None

url_video_out = ""
clip_name_out = ""

def setup(setupFile):
    global url_backgroundVideo_in, url_img_in, url_audio_in, texts_in
    global url_video_out, clip_name_out
    global duration_video, words_in_line, videoCount, url_font, text_p

    inputJson = database.json_read("input", setupFile)
    outputJson = database.json_read("output", setupFile)
    sysJson = database.json_read("sys", setupFile)

    url_backgroundVideo_in = inputJson["videoFile"]
    url_img_in = inputJson["imgFile"]
    url_audio_in = inputJson["audioFile"]
    texts_in = inputJson["text"]

    url_video_out = outputJson["videoPath"]
    clip_name_out = outputJson["clipName"]

    duration_video = sysJson["duration"]
    words_in_line = sysJson["wordInLine"]
    videoCount = sysJson["videoCount"]
    url_font = sysJson["textFont"]
    text_p = sysJson["textHeight_p"]

if __name__ == "__main__":
    setup(input("choose json setup file: "))
    create_video = SCC(duration_video, words_in_line, url_font)
    create_video.text_p = text_p
    video_count = 0
    while video_count != videoCount:
        #       VIDEO
        if url_backgroundVideo_in[1] != 0:
            ran = random.randint(0, url_backgroundVideo_in[1])
        else:
            ran = 0
        create_video.AddVideoClip(f"{url_backgroundVideo_in[0]}{ran}.mp4")

        #       TEXT
        video_text_db = database.json_read(texts_in[1], texts_in[0])
        if len(video_text_db) != 1:
            text = video_text_db[random.randint(0, len(video_text_db)-1)]
        else:
            text = video_text_db[0]

        text_element_position = create_video.AddText(text)
        print(f"text element position: {text_element_position}")

        #       IMG
        if url_img_in != None:
            create_video.AddImg(url_img_in)

        #       AUDIO
        if url_audio_in == "VA":
            pass
        elif url_audio_in == None:
            create_video.video = create_video.video.without_audio()
        else:
            if url_audio_in[1] != 0:
                ran = random.randint(0, url_audio_in[1])
            else:
                ran = 0
            clip_audio = create_video.NewAudioClip(f"{url_audio_in[0]}{ran}.mp3")
            # additional options
            if url_audio_in[2][0] == "OL":
                create_video.AddAudioClip([create_video.video.audio, clip_audio], 1)
                # OL -> overlay
            elif url_audio_in[2][0] == "R":
                pass
                # R -> replace
                create_video.AddAudioClip(clip_audio, 1)

        #       CREATING CLIP
        create_video.CreateVideo(clip_name_out + str(video_count), url_video_out)

        video_count += 1
