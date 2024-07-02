from gradio_client import Client, handle_file
import requests
import os
import json
import shutil
import random

# Text-To-Image Generation
def Image(prompt, to_avoid = "lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry", changed = False):
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
	shutil.move(path, os.path.join('static', "img.png"))
	return os.path.join('static', "img.png")


# Text-to-Speech Generation
def Speech(prompt, language, voice, gender, changed = False):
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
	
	shutil.move(path, os.path.join('static', "aud.mp3"))
	return os.path.join('static', "aud.mp3")



# Text-to-Video Generation
def Video(prompt, changed = False):
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
	shutil.move(path, os.path.join('static', "vid.mp4"))
	return os.path.join('static', "vid.mp4")

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
def generate_sound_effect(prompt):
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

class Content():
	def __init__(self, image_prompt, video_prompt, speech_prompt, language = "English", voice = False, gender = "F"):
		self.image = Image(image_prompt)
		self.video = Video(video_prompt)
		self.speech = Speech(speech_prompt, language, voice, gender)
		self.prompts = [image_prompt, video_prompt, speech_prompt]
		self.options = [language, voice, gender]
		self.changed_image, self.changed_video, self.changed_audio = False, False, False
	def changed(self, change_image, change_video, change_audio):
		if change_image:
			self.changed_image = not self.changed_image
			self.image = Image(self.prompts[0], self.changed_image)
		if change_video:
			self.changed_video = not self.changed_video
			self.video = Video(self.prompts[1], self.changed_video)
		if change_audio:
			self.changed_audio = not self.changed_audio
			self.speech = Speech(self.prompts[2], self.options[0], self.options[1], self.options[2], self.changed_audio)

