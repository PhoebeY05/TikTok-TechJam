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
# Text-To-Image Generation
def generate_image(prompt, to_avoid, changed = False):
	if changed:
		client = Client("Aqcua/TextToImage-AISDXLTURBO")
		result = client.predict(
				prompt=prompt,
				negative_prompt=to_avoid,
				seed=0,
				randomize_seed=True,
				width=512,
				height=512,
				guidance_scale=0,
				num_inference_steps=2,
				api_name="/infer"
		)
		path = result
	else:
		client = Client("stabilityai/stable-diffusion-3-medium")
		result = client.predict(
				prompt=prompt,
				negative_prompt=to_avoid,
				seed=0,
				randomize_seed=True,
				width=1024,
				height=1024,
				guidance_scale=5,
				num_inference_steps=28,
				api_name="/infer"
		)
		path = result[0]
	shutil.move(path, os.path.join(content_folder, "img.png"))
	return os.path.join(content_folder, "img.png")


# Text-to-Speech Generation
def generate_speech(prompt, language, voice, gender, changed = False, sid=0):
	if voice:
		if changed:
			client = Client("mhemanthkmr143/text_to_speech")
			result = client.predict(
				wav_file=handle_file(voice),
				text=prompt,
				api_name="/predict"
			)
		else:
			client = Client("tonyassi/voice-clone")
			result = client.predict(
					text=prompt,
					audio=handle_file(voice),
					api_name="/predict"
			)
		path = result	
	else:
		client = Client("k2-fsa/text-to-speech")
		if gender == "F": # Female voice
			if language == "English":
				model = "csukuangfj/vits-piper-en_GB-southern_english_female-medium|6 speakers"
			elif language == "Chinese (Mandarin, 普通话)":
				model = "csukuangfj/vits-zh-hf-bronya|804"
				if changed: 
					model = "csukuangfj/vits-zh-hf-theresa|804"
			else:
				model = "csukuangfj/vits-cantonese-hf-xiaomaiiwn"
		elif gender == "M": # Male voice
			if language == "English":
				model = "csukuangfj/vits-piper-en_GB-southern_english_male-medium|8 speakers"	
			elif language == "Chinese (Mandarin, 普通话)":
				model = "csukuangfj/vits-zh-hf-fanchen-wnj|1"
				if changed: 
					model = "csukuangfj/vits-zh-hf-fanchen-C|187"
		result = client.predict(
			language=language,
			repo_id=model,
			text=prompt,
			sid=str(sid),
			speed=1,
			api_name="/process"
		)
		path = result[0]
	
	shutil.move(path, os.path.join(content_folder, "aud.mp3"))
	return os.path.join(content_folder, "aud.mp3")



# Text-to-Video Generation
def generate_video(prompt, changed = False):
	if changed:
		client = Client("BestWishYsh/MagicTime")
		result = client.predict(
				dreambooth_dropdown="RcnzCartoon.safetensors",
				motion_module_dropdown="motion_module.ckpt",
				prompt_textbox=prompt,
				negative_prompt_textbox="worst quality, low quality, nsfw, logo",
				width_slider=512,
				height_slider=512,
				seed_textbox="-1",
				api_name="/magictime"
		)
		path = result[0]['value']['video']
	else:
		client = Client("https://videocrafter-videocrafter.hf.space/")
		result = client.predict(
			prompt,	# str in 'Prompts' Textbox component
			50,	# int | float (numeric value between 1 and 60) in 'Sampling steps' Slider component
			12,	# int | float (numeric value between 1.0 and 30.0) in 'CFG Scale' Slider component
			1,	# int | float (numeric value between 0.0 and 1.0) in 'ETA' Slider component
			16,	# int | float (numeric value between 4 and 32) in 'fps' Slider component
			fn_index=1
		)
		path = result
	shutil.move(path, os.path.join(content_folder, "vid.mp4"))
	return os.path.join(content_folder, "vid.mp4")

# Sound Effect
def generate_sound_effect(prompt, changed = False):
	if changed:
		client = Client("https://haoheliu-audioldm2-text2audio-text2music.hf.space/")
		result = client.predict(
			prompt,	# str in 'Input text' Textbox component
			"low quality, extra limbs, floating",	# str in 'Negative prompt' Textbox component
			10,	# int | float (numeric value between 5 and 15) in 'Duration (seconds)' Slider component
			3.5,	# int | float (numeric value between 0 and 7) in 'Guidance scale' Slider component
			45,	# int | float in 'Seed' Number component
			3,	# int | float (numeric value between 1 and 5) in 'Number waveforms to generate' Slider component
			fn_index=1
		)
	else:
		client = Client("eagle0504/stable-audio-demo")
		result = client.predict(
			prompt,
			seconds_total=30,
			steps=100,
			cfg_scale=7,
			randomize_seed=True,
			seed=2093631713,
			api_name="/predict"
		)
	
	path = result
	shutil.move(path, os.path.join(content_folder, "effect.mp3"))
	return os.path.join(content_folder, "effect.mp3")


# resize function was copied from https://stackoverflow.com/questions/44370469/python-image-resizing-keep-proportion-add-white-background
def resize(image_pil, width, height):
    '''
    Resize PIL image keeping ratio and using white background.
    '''
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize((resize_width, resize_height), Image.LANCZOS)
    background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background.convert('RGB')
		
def Result(image_path, video_path, audio_path, sound_effect_path, priority = "Audio", user = False):
	
	# Duplicating video for both final result and original video to exist
	if user:
		result_path = video_path
	else:
		source_file = open(video_path, 'rb')
		result_path = os.path.join(content_folder, "result.mp4")
		destination_file = open(result_path, 'wb')
		shutil.copyfileobj(source_file, destination_file)

	# Trimming to ensure same duration
	video = VideoFileClip(result_path)
	audio = AudioFileClip(audio_path)
	image_duration = 1
	if priority == "Audio":
		if video.duration > audio.duration:
			video_trim(result_path, audio, sound_effect_path)
		elif (audio.duration - video.duration) > 1:
			image_duration = audio.duration - video.duration
	else:
		audio_trim(video, audio_path, sound_effect_path)

	os.system(f"rm -rf {content_folder}/trim*.mp3")
	os.system(f"rm -rf {content_folder}/trim*.mp4")

	# Resizing image to use as thumbnail
	capture=cv2.VideoCapture(video_path) 
	width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
	img = Image.open(image_path)
	img = resize(img, int(width), int(height))
	img.save(image_path)

	# Combining image and video
	image = ImageClip(image_path).set_duration(image_duration)
	combine = concatenate_videoclips([image, video])
	combine.write_videofile(result_path)

	# Combining video and audio
	result = video.set_audio(audio)
	result.write_videofile(result_path)

	# Combining video and sound_effect
	if sound_effect_path:
		video = VideoFileClip(result_path)
		sound_effect = AudioFileClip(sound_effect_path)
		final_audio = CompositeAudioClip([video.audio, sound_effect])
		result = video.set_audio(final_audio)
		result.write_videofile(result_path)

	return result_path

class Content():
	def __init__(self, image_prompt,video_prompt, speech_prompt, negative_prompt, effect_prompt = "", language = "English", voice = False, gender = "F"):
		self.image = generate_image(image_prompt, negative_prompt)
		self.video = generate_video(video_prompt)
		self.speech = generate_speech(speech_prompt, language, voice, gender)
		if not effect_prompt:
			self.sound_effect = False
		else:
			self.sound_effect = generate_sound_effect(effect_prompt)
		self.prompts = [image_prompt, video_prompt, speech_prompt, negative_prompt, effect_prompt]
		self.options = [language, voice, gender]
		self.changed_image, self.changed_video, self.changed_audio, self.changed_effect = False, False, False, False
		self.result = ""
		

	def changed(self, change_image, change_video, change_audio, change_effect, sid):
		new = 0
		if change_image:
			self.changed_image = not self.changed_image
			self.image = generate_image(self.prompts[0], self.prompts[3], self.changed_image)
		if change_video:
			self.changed_video = not self.changed_video
			self.video = generate_video(self.prompts[1], self.changed_video)
		if change_audio:
			if self.options[0] == "English":
				while new == sid:
					new = random.randint(0, 5)
			self.changed_audio = not self.changed_audio
			self.speech = generate_speech(self.prompts[2], self.options[0], self.options[1], self.options[2], self.changed_audio, new)
		if change_effect:
			self.changed_effect = not self.changed_effect
			self.sound_effect = generate_sound_effect(self.prompts[4], self.changed_effect)
		return new
	def generate_result(self):
		self.result = Result(self.image, self.video, self.speech, self.sound_effect)
		return self.result