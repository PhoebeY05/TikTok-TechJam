from models import SummariseYoutubeVideo, IdentifyText, Content
from flask import Flask, redirect, session, render_template, request, flash, url_for
from flask_session import Session
import os
import time
import threading

lock = threading.Lock()

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['uploadFolder'] = 'static/upload'
Session(app)


@app.route("/", methods = ["GET", "POST"])
def home():
	if request.method == "POST":
		image_prompt = request.form.get("image_prompt")
		video_prompt = request.form.get("video_prompt")
		speech_prompt = request.form.get("speech_prompt")
		language = request.form.get("language")
		voice_file = request.files["voice_file"]
		voice_url = request.form.get("voice_url")
		gender = request.form.get("gender")
		if image_prompt and video_prompt and speech_prompt:
			if not language:
				language = "English"
			if not gender:
				gender = "F"
			if voice_file or (voice_file and voice_url):
				voice_file.save(os.path.join(app.config['uploadFolder'], voice_file.filename))
				voice = os.path.join(app.config['uploadFolder'], voice_file.filename)
			elif voice_url:
				voice = voice_url
			else:
				voice = False
			content = Content(image_prompt, video_prompt, speech_prompt, language, voice, gender)
			image = content.image
			video = content.video
			speech = content.speech
			session["content"] = content
			return render_template("results.html", image=image, video=video, speech=speech)
		else:
			flash("Must fill in all the prompts")
			return render_template("home.html")
	else:
		os.system(f'rm -rf {app.config['uploadFolder']}/*') # removing contents of upload folder to ensure user privacy
		return render_template("home.html")
@app.route("/insights", methods = ["GET", "POST"])
def insights():
	if request.method == "POST":
		image = request.files["image"]
		video = request.form.get("video")
		if image and video:
			summary = SummariseYoutubeVideo(video)
			image.save(os.path.join(app.config['uploadFolder'], image.filename))
			text = IdentifyText(os.path.join(app.config['uploadFolder'], image.filename))
			return render_template("insights.html", text=text, summary=summary)
		elif image:
			image.save(os.path.join(app.config['uploadFolder'], image.filename))
			text = IdentifyText(os.path.join(app.config['uploadFolder'], image.filename))
			return render_template("insights.html", text=text)
		elif video:
			summary = SummariseYoutubeVideo(video)
			return render_template("insights.html", summary=summary)
		else:
			return render_template("insights.html", text="", summary="")
	else:
		text = ""
		return render_template("insights.html", text=text)

@app.route("/change", methods = ["POST"])
def change():
	change_image = request.form.get("change_image")
	change_video = request.form.get("change_video")
	change_audio = request.form.get("change_audio")
	content = session["content"]
	content.changed(change_image, change_video, change_audio)
	image = content.image
	video = content.video
	speech = content.speech
	session["content"] = content
	return render_template("results.html", image=image, video=video, speech=speech)

@app.route("/results")
def results():
	if "content" in session:
		content = session["content"]
		image = content.image
		video = content.video
		speech = content.speech
		return render_template("results.html", image=image, video=video, speech=speech)
	else:
		return render_template("error.html")
	
	
def create_app():
   return app