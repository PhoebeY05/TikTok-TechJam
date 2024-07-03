from gradio_client import Client, handle_file
import requests
import os
import json
import shutil
import random
from moviepy.editor import *
import math
import ffmpeg
import cv2
from PIL import Image


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
def generate_speech(prompt, language, voice, gender, changed = False):
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
		sid = 0
		if language == "English" and changed:
			sid = random.randint(0, 5)
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
			else:
				model = "csukuangfj/vits-cantonese-hf-xiaomaiiwn"
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

#Text in Image
def IdentifyText(image):
	client = Client("gokaygokay/Florence-2")
	result = client.predict(
			image=handle_file(image),
			task_prompt="OCR",
			text_input=None,
			model_id="microsoft/Florence-2-large",
			api_name="/process_image"
	)
	text = result[0].replace("'", '"')
	dictionary = json.loads(text)
	text = dictionary['<OCR>'].replace("\n", " ")
	return text


# Video Summariser
def SummariseYoutubeVideo(video):
	r = requests.post(url="https://sudarshanar-videosummaryfromyoutubevideo.hf.space/api/predict", json={"data": [video,"BART"]})
	return r.json()['data'][0]

# Sound Effect
def generate_sound_effect(prompt, changed = False):
	if changed:
		client = Client("https://haoheliu-audioldm2-text2audio-text2music.hf.space/")
		result = client.predict(
			prompt,	# str in 'Input text' Textbox component
			"low quality",	# str in 'Negative prompt' Textbox component
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

# center_crop function uses the code in https://medium.com/curious-manava/center-crop-and-scaling-in-opencv-using-python-279c1bb77c74

def center_crop(img, dim):
	img = cv2.imread(img)
	width, height = img.shape[1], img.shape[0]
	# process crop width and height for max available dimension
	crop_width = dim[0] if dim[0]<img.shape[1] else img.shape[1]
	crop_height = dim[1] if dim[1]<img.shape[0] else img.shape[0] 
	mid_x, mid_y = int(width/2), int(height/2)
	cw2, ch2 = int(crop_width/2), int(crop_height/2) 
	crop_img = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
	image = Image.fromarray(crop_img)
	image.save(os.path.join(content_folder, "thumbnail.jpg"))
	return os.path.join(content_folder, "thumbnail.jpg")



def Result(image, video, audio, sound_effect):
	capture=cv2.VideoCapture(video) 
	# Duplicating video for both final result and original video to exist
	source_file = open(video, 'rb')
	result_path = os.path.join(content_folder, "result.mp4")
	destination_file = open(result_path, 'wb')
	shutil.copyfileobj(source_file, destination_file)
	video = VideoFileClip(result_path)

	# Trimming audio files to fit video's duration
	duration = video.duration
	# Speech
	audio_input = ffmpeg.input(audio)
	audio_cut = audio_input.audio.filter('atrim', duration=duration)
	audio_output = ffmpeg.output(audio_cut, os.path.join(content_folder, "trim_speech.mp3"))
	ffmpeg.run(audio_output)
	# Sound effect
	if sound_effect:
		audio_input = ffmpeg.input(sound_effect)
		audio_cut = audio_input.audio.filter('atrim', duration=duration)
		audio_output = ffmpeg.output(audio_cut, os.path.join(content_folder, "trim_effect.mp3"))
		ffmpeg.run(audio_output)
	os.system(f"rm -rf {content_folder}/trim*.mp3")

	# Combining video and audio
	audio = AudioFileClip(audio)
	result = video.set_audio(audio)
	result.write_videofile(result_path)

	# Combining video and sound_effect
	if sound_effect:
		video = VideoFileClip(result_path)
		sound_effect = AudioFileClip(sound_effect)
		final_audio = CompositeAudioClip([video.audio, sound_effect])
		result = video.set_audio(final_audio)
		result.write_videofile(result_path)

	# Using image as thumbnail
	width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
	image_path = center_crop(image, (width, height))
	image = ImageClip(image_path).set_duration(1)
	image = image.subclip(0, image.end).fx(vfx.fadeout, .5, final_color=[87, 87, 87])
	video = video.subclip(0, video.end).fx(vfx.fadein, .5, initial_color=[87, 87, 87])
	combine = concatenate_videoclips([image, video])
	combine.write_videofile(result_path)
	return result_path

class Content():
	def __init__(self, image_prompt,video_prompt, speech_prompt, negative_prompt = "lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry", effect_prompt = "", language = "English", voice = False, gender = "F"):
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
		

	def changed(self, change_image, change_video, change_audio, change_effect):
		if change_image:
			self.changed_image = not self.changed_image
			self.image = generate_image(self.prompts[0], self.prompts[3], self.changed_image)
		if change_video:
			self.changed_video = not self.changed_video
			self.video = generate_video(self.prompts[1], self.changed_video)
		if change_audio:
			self.changed_audio = not self.changed_audio
			self.speech = generate_speech(self.prompts[2], self.options[0], self.options[1], self.options[2], self.changed_audio)
		if change_effect:
			self.changed_effect = not self.changed_effect
			self.sound_effect = generate_sound_effect(self.prompts[4], self.changed_effect)
	def generate_result(self):
		self.result = Result(self.image, self.video, self.speech, self.sound_effect)
		return self.result