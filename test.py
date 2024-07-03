import moviepy.editor as mpe
from ffmpy import FFmpeg
import shutil 
import os
from models import Result

content_folder = 'static/content'
video = os.path.join(content_folder, "vid.mp4")
audio = os.path.join(content_folder, "aud.mp3")
sound_effect = os.path.join(content_folder, "effect.mp3")
image = os.path.join(content_folder, "img.png")

Result(image, video, audio, sound_effect)