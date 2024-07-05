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

client = Client("eagle0504/stable-audio-demo")
result = client.predict(
    "dog barking",
    seconds_total=30,
    steps=100,
    cfg_scale=7,
    randomize_seed=True,
    seed=2093631713,
    api_name="/predict"
)