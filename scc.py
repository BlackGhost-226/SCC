import moviepy.editor as mp
import cv2


class SCC:
    def __init__(self, duration_video, words_in_line, url_font, text_p):
        self.duration_video = duration_video
        self.words_in_line = words_in_line
        self.url_font = url_font
        self.text_p = text_p
        self.resolution = ()

        self.video = None
        self.clipElementsList = []

    def SplitText(self, text):
        print("splitting text")
        if len(text.split(" ")) <= self.words_in_line:
            print("if")
            return text
        else:
            print("else")
            main_text = ""
            words = text.split(" ")
            counter = 0
            for i in words:
                if counter == self.words_in_line:
                    main_text = main_text + f"\n{i}"
                    counter = 0
                    print("counter:0")
                else:
                    main_text = main_text + f" {i}"
                counter = counter + 1
                print(f"counter:{counter}")
            return main_text

    def AddVideoClip(self, videoUrl):
        video = mp.VideoFileClip(videoUrl)

        vid = cv2.VideoCapture(videoUrl)
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))

        print(f"video resolution: {width}x{height}")
        self.resolution = (width, height)

        if video.duration < self.duration_video:
            self.duration_video = video.duration

        clip_video = video.subclip(0, self.duration_video)

        clip_video = clip_video.resize(self.resolution)

        self.video = clip_video

        print(f"video real resolution: {self.video.w}x{self.video.h}")

    def AddText(self, text):
        text_element_position = (self.video.h / 2160) * self.text_p

        clip_text = mp.TextClip(txt=self.SplitText(text),
                                fontsize=70,
                                font=self.url_font,
                                color="white",
                                bg_color="black",
                                align="center")

        clip_text = clip_text.set_position(("center", text_element_position))
        clip_text = clip_text.set_duration(self.duration_video)
        self.clipElementsList.append(clip_text)

        print(f"text element position: {text_element_position}")

    def AddImg(self, imgUrl):
        clip_img = mp.ImageClip(imgUrl)
        clip_img = clip_img.set_position(("left", "top"))
        clip_img = clip_img.set_duration(self.duration_video)

        self.clipElementsList.append(clip_img)

    def NewAudioClip(self, audioUrl):
        clip_audio = mp.AudioFileClip(audioUrl)
        clip_audio = clip_audio.subclip(0, self.duration_video)
        return clip_audio

    def AddAudioClip(self, audio, maxVol):
        clip_audio = None

        if type(audio) is list:
            clip_audio = mp.CompositeAudioClip(audio)

        clip_audio = clip_audio.subclip(0, self.duration_video)
        clip_audio = clip_audio.max_volume(maxVol)

        self.video = self.video.with_audio(clip_audio)

    def CreateVideo(self, videoName, videoUrl):
        self.clipElementsList.insert(0, self.video)

        print("---| Debugging is working |---")
        for i, clip in enumerate(self.clipElementsList):
            try:
                print(f"Debug: Clip {i}: duration={clip.duration}, filename={clip.filename}")
            except Exception as e:
                print(f"Debug: Error with clip {i}: {e}")

        print("---| Moviepy is working |---")
        # clips_array, concatenate_videoclips, CompositeVideo
        final_clip = mp.CompositeVideoClip(clips=self.clipElementsList, size=self.resolution)
        final_clip.write_videofile(f"{videoUrl}\\{videoName}.mp4", codec="libx264", fps=self.video.fps)
