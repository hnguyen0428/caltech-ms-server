import imageio
import numpy as np
from moviepy.editor import *
from conf import base_url, VIDEOS_FOLDER, EDITED_VIDEOS_FOLDER

imageio.plugins.ffmpeg.download()

class HighlightMaker():
    def __init__(self, videosPath=VIDEOS_FOLDER, editedVideosPath=EDITED_VIDEOS_FOLDER):
        self.videosPath = videosPath
        self.editedVideosPath = editedVideosPath
        self.videoFilename = None
        self.videoClip = None
        self.chunkSize = 10

    def useFile(self, videoFilename):
        self.videoFilename = videoFilename
        self.videoClip = VideoFileClip(self.videosPath + videoFilename)

    def extractVolumeArray(self, videoFilename=None):

        if(videoFilename):
            self.useFile(videoFilename)

        if not self.videoClip:
            return None

        cut = lambda i: self.videoClip.audio.subclip(i, i + 1).to_soundarray(fps=22000)
        volume = lambda array: np.sqrt(((1.0 * array) ** 2).mean())
        volumes = [volume(cut(i)) for i in range(0, int(self.videoClip.audio.duration - 1))]
        return volumes

    def _adjustAudioLevel(self):

        # find volumes of the clip
        volumes = self.extractVolumeArray()
        max_volume = max(volumes)

        # adjust audio levels
        ratio = 1

        while (max_volume > 0.05):
            print("Current audio is high, reducing volume...")
            ratio -= 0.05
            max_volume = max_volume * ratio

        while (max_volume < 0.005):
            print("Current audio is low, increasing volume...")
            ratio += 0.05
            max_volume = max_volume * ratio

        self.videoClip = self.videoClip.volumex(ratio)

    def extractHighlight(self, videoFilename=None, write=True):

        if (videoFilename):
            self.useFile(videoFilename)

        if not self.videoClip:
            return None

        self._adjustAudioLevel()
        volumes = self.extractVolumeArray()

        #set the threshold minimum volume to keep
        threshold = np.log(volumes).mean()

        #array of which seconds to keep in the video
        includes = [False for i in range(int(self.videoClip.duration))]

        for i in range(len(volumes)):
            volume = volumes[i:i + self.chunkSize]
            if (np.log(volume).mean() > threshold):
                includes[i] = True

        include_ranges = []
        s = -1
        e = -1
        for i in range(len(includes)):

            #calculate the highlights to include
            if (includes[i]):
                if(s <= e):
                    s = i
            else:
                #check if e has been set to be before s, and if snippets are 4+ secs
                if(s > e and i-s > 4):
                    e = i
                    include_ranges.append((s, e))
                else:
                    e = s

        print(include_ranges)
        fade_duration = 1  # 1-second fade-in for each clip

        #create the subclips, then merge them together (with fading transitions)
        subclips = []
        for include in include_ranges:
            print(include[1]-include[0])
            subclips.append(self.videoClip.subclip(include[0], include[1]))

        clips = [clip.crossfadein(fade_duration) for clip in subclips]
        clip = concatenate_videoclips(subclips, padding=-fade_duration)

        print("The new video is {} seconds long".format(clip.duration))

        #write out new video if we want to
        if write:
            clip.write_videofile(self.editedVideosPath + self.videoFilename, temp_audiofile="temp-audio.m4a", remove_temp=True,
                             codec="libx264", audio_codec="aac")

            wavFile = videoFilename.split(".")[0] + ".wav"
            clip.audio.write_audiofile(self.editedVideosPath + wavFile)

        return clip