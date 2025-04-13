import database
import requests
import random
import moviepy as mp
import sys
import os

duration_video = 15
words_in_line = 3
videoCount = -1
url_font = None
text_p = 1900

url_backgroundVideo_in = None
url_img_in = None
url_audio_in = None
texts_in = None

url_video_out = None
clip_name_out = None

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

def split_text(text):
    global words_in_line
    print("splitting text")
    if len(text.split(" ")) <= words_in_line:
        print("if")
        return text
    else:
        print("else")
        main_text = ""
        words = text.split(" ")
        counter = 0
        for i in words:
            if counter == words_in_line:
                main_text = main_text + f"\n{i}"
                counter = 0
                print("counter:0")
            else:
                main_text = main_text + f" {i}"
            counter = counter + 1
            print(f"counter:{counter}")
        return main_text

def create_video(clip_name):
    global duration_video, text_p, url_font # sys

    global url_backgroundVideo_in, url_img_in, texts_in, url_audio_in # input

    global url_video_out # output
    print("---| Debugging is working |---")

    clips_list_elements = []

    #       VIDEO
    if url_backgroundVideo_in[1] != 0:
        ran = random.randint(0, url_backgroundVideo_in[1])
    else:
        ran = 0
    video = mp.VideoFileClip(f"{url_backgroundVideo_in[0]}{ran}.mp4")

    if video.duration < duration_video:
        duration_video = video.duration

    clip_video = video.subclipped(0, duration_video)

    #       TEXT
    # font="Amiri-Bold", color="black", stroke_width=4, method="caption", align="center", size=(170, 73)

    if texts_in != None:
        text_element_position = (video.h/2160)*text_p
        print(f"text element position: {text_element_position}")

        video_text_db = database.json_read(texts_in[1], texts_in[0])

        if len(video_text_db) != 1:
            text = video_text_db[random.randint(0, len(video_text_db)-1)]
        else:
            text = video_text_db[0]

        clip_text = mp.TextClip(text=split_text(text), font_size=70, font=url_font, color="white", bg_color="black", text_align="center")

        clip_text = clip_text.with_position(("center", text_element_position))
        clip_text = clip_text.with_duration(duration_video)
        clips_list_elements.append(clip_text)

    #       IMG
    if url_img_in != None:
        clip_img = mp.ImageClip(url_img_in)
        clip_img = clip_img.with_position(("left", "top")).with_duration(duration_video)
        clips_list_elements.append(clip_img)

    #       AUDIO
    if url_audio_in == "VA":
        pass
        # clip_audio = clip_video.audio
        # clip_video = clip_video.without_audio()        
        # clip_audio = mp.AudioFileClip(clip_audio)
        # clips_list_elements.append(clip_audio)
    elif url_audio_in == None:
        clip_video = clip_video.without_audio()
    # elif len(url_audio_in) == 3 and type(url_audio_in[2]) is list:
    else:
        if url_audio_in[1] != 0:
            ran = random.randint(0, url_audio_in[1])
        else:
            ran = 0
        clip_audio = mp.AudioFileClip(filename=f"{url_audio_in[0]}{ran}.mp3")
        clip_audio = clip_audio.subclipped(0, duration_video)
        # additional options
        if url_audio_in[2][0] == "OL":
            clip_audio = mp.CompositeAudioClip([clip_video.audio, clip_audio])
            # OL -> overlay
        elif url_audio_in[2][0] == "R":
            pass
            # R -> replace
            clip_audio = clip_audio.with_volume_scaled(url_audio_in[2][1])
        clip_video = clip_video.with_audio(clip_audio)
    

    #       CREATING CLIP
    clips_list = [clip_video]
    for i in clips_list_elements:
        clips_list.append(i)

    for i, clip in enumerate(clips_list):
        try:
            print(f"Debug: Clip {i}: duration={clip.duration}, filename={clip.filename}")
        except Exception as e:
            print(f"Debug: Error with clip {i}: {e}")
    print("---| Moviepy is working |---")

    # clips_array, concatenate_videoclips, CompositeVideo
    final_clip = mp.CompositeVideoClip(clips_list)
    final_clip.write_videofile(f"{url_video_out}\\{clip_name}.mp4")

if __name__ == "__main__":
    setup(input("choose json setup file: "))
    video_count = 0
    while video_count != videoCount:
        create_video(f"{clip_name_out}{video_count}")
        video_count += 1
