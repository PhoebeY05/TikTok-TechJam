from models import SummariseYoutubeVideo, IdentifyText, Content
from flask import Flask, redirect, session, render_template, request, flash, url_for
from flask_session import Session
import os
import time


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['uploadFolder'] = 'static/upload'
app.config['contentFolder'] = 'static/content'

Session(app)


@app.route("/", methods = ["GET", "POST"])
def home():
	if request.method == "POST":
		os.system(f"rm -rf {app.config['contentFolder']}/*")
		session["generated"] = True
		image_prompt = request.form.get("image_prompt")
		negative_prompt = request.form.get("negative_prompt")
		video_prompt = request.form.get("video_prompt")
		speech_prompt = request.form.get("speech_prompt")
		effect_prompt = request.form.get("effect_prompt")
		language = request.form.get("language")
		voice_file = request.files["voice_file"]
		voice_url = request.form.get("voice_url")
		gender = request.form.get("gender")
		session["sid"] = 0
		if image_prompt and video_prompt and speech_prompt:
			# Optional inputs
			if not language:
				language = "English"				
			if not gender:
				gender = "F"
			if not effect_prompt:
				effect_prompt = ""
			if not negative_prompt:
				negative_prompt = "lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"
			if voice_file or (voice_file and voice_url):
				voice_file.save(os.path.join(app.config['uploadFolder'], voice_file.filename))
				voice = os.path.join(app.config['uploadFolder'], voice_file.filename)
			elif voice_url:
				voice = voice_url
			else:
				voice = False
			# Generating content with inputs
			content = Content(image_prompt, video_prompt, speech_prompt, negative_prompt, effect_prompt, language, voice, gender)
			session["content"] = content
			image = content.image
			video = content.video
			speech = content.speech
			language = content.options[0]
			if effect_prompt:
				sound_effect = content.sound_effect
				return render_template("results.html", image=image, video=video, speech=speech, sound_effect=sound_effect, language=language)
			return render_template("results.html", image=image, video=video, speech=speech, language=language)
		else:
			flash("Must fill in all the prompts")
			return render_template("home.html")
	else:
		os.system(f"rm -rf {app.config['contentFolder']}/*") # removing contents of content folder to ensure user privacy
		return render_template("home.html")
@app.route("/media", methods = ["GET", "POST"])
def media():
	if request.method == "POST":
		image = request.files["image"]
		video = request.form.get("video")
		if image and video:
			summary = SummariseYoutubeVideo(video)
			image.save(os.path.join(app.config['uploadFolder'], image.filename))
			text = IdentifyText(os.path.join(app.config['uploadFolder'], image.filename))
			return render_template("media.html", text=text, summary=summary)
		elif image:
			image.save(os.path.join(app.config['uploadFolder'], image.filename))
			text = IdentifyText(os.path.join(app.config['uploadFolder'], image.filename))
			return render_template("media.html", text=text)
		elif video:
			summary = SummariseYoutubeVideo(video)
			return render_template("media.html", summary=summary)
		else:
			return render_template("media.html", text="", summary="")
	else:
		return render_template("media.html")

@app.route("/change", methods = ["POST"])
def change():
	change_image = request.form.get("change_image")
	change_video = request.form.get("change_video")
	change_audio = request.form.get("change_audio")
	change_effect = request.form.get("change_effect")
	content = session["content"]
	content.changed(change_image, change_video, change_audio, change_effect, session["sid"])
	session["content"] = content
	image = content.image
	video = content.video
	speech = content.speech
	sound_effect = content.sound_effect
	language = content.options[0]
	if sound_effect:
		return render_template("results.html", image=image, video=video, speech=speech, sound_effect=sound_effect, language=language)
	else:
		return render_template("results.html", image=image, video=video, speech=speech, language=language)

@app.route("/results", methods = ["GET", "POST"])
def results():
	if request.method == "POST":
		content = session["content"]
		result = content.generate_result()
		session["content"] = content
		return render_template("video.html", result=result)
	else:
		if "generated" in session:
			content = session["content"]
			image = content.image
			video = content.video
			speech = content.speech
			sound_effect = content.sound_effect
			result = content.result
			language = content.options[0]
			if sound_effect and result:
				return render_template("results.html", image=image, video=video, speech=speech, sound_effect=sound_effect, result=result, language=language)
			elif result:
				return render_template("results.html", image=image, video=video, speech=speech, result=result, language=language)
			elif sound_effect:
				return render_template("results.html", image=image, video=video, speech=speech, sound_effect=sound_effect, language=language)
			else:
				return render_template("results.html", image=image, video=video, speech=speech, language=language)
		else:
			return render_template("error.html")

@app.route("/video", methods = ["GET", "POST"])
def video():
	content = session["content"]
	result = content.result
	return render_template("video.html", result=result)
def create_app():
   return app