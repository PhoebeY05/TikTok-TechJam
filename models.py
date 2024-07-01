from gradio_client import Client, handle_file
import requests
import json

# Text-To-Image Generation
def Image(prompt, to_avoid = "lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry", changed = False):
	client = Client("Aqcua/TextToImage-AISDXLTURBO")
	if changed:
		result = client.predict(
				prompt="Hello!!",
				negative_prompt="Hello!!",
				seed=0,
				randomize_seed=True,
				width=512,
				height=512,
				guidance_scale=0,
				num_inference_steps=2,
				api_name="/infer"
		)
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
	return result


# Text-to-Speech Generation
def Speech(prompt, language, voice = False, changed = False):
	if voice:
		client = Client("tonyassi/voice-clone")
		result = client.predict(
				text=prompt,
				audio=handle_file(voice),
				api_name="/predict"
		)
	else:
		if changed:
			client = Client("tonyassi/voice-clone")
			result = client.predict(
					text=prompt,
					audio=handle_file("../static/default.wav"),
					api_name="/predict"
			)
		else:
			client = Client("Flux9665/MassivelyMultilingualTTS")
			result = client.predict(
					prompt=prompt,
					language=language,
					voice_seed=279,
					duration_scaling_factor=1,
					pitch_variance_scale=1,
					energy_variance_scale=1,
					emb1=0,
					emb2=0,
					api_name="/predict"
			)	
			return result[0]
	return result



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
	else:
		client = Client("https://videocrafter-videocrafter.hf.space/")
		result = client.predict(
			prompt,	# str in 'Prompts' Textbox component
			1,	# int | float (numeric value between 1 and 60) in 'Sampling steps' Slider component
			1,	# int | float (numeric value between 1.0 and 30.0) in 'CFG Scale' Slider component
			0,	# int | float (numeric value between 0.0 and 1.0) in 'ETA' Slider component
			4,	# int | float (numeric value between 4 and 32) in 'fps' Slider component
			fn_index=1
		)
	return result


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

