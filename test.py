from gradio_client import Client, handle_file
import requests
import os
import json
import shutil
import random
from moviepy.editor import *
import math
import cv2
from PIL import Image
from trim import audio_trim, video_trim

content_folder = 'static/content'
result_path = os.path.join(content_folder, "result.mp4")
audio_path = os.path.join(content_folder, "aud.mp3")
video = VideoFileClip(result_path)
audio = AudioFileClip(audio_path)
result = video.set_audio(audio)
result.write_videofile(result_path)