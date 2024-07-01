from models import Image, Speech, Video, SummariseYoutubeVideo, IdentifyText
from flask import Flask, redirect, session, render_template, request, flash, url_for
from flask_session import Session
import os

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

Upload = 'static/upload'
app.config['uploadFolder'] = Upload

@app.route("/", methods = ["GET", "POST"])
def home():
	if request.method == "POST":
		image_prompt = request.form.get("image_prompt")
		video_prompt = request.form.get("video_prompt")
		speech_prompt = request.form.get("speech_prompt")
		language = request.form.get("language")
		voice_file = request.files["voice_file"]
		voice_url = request.form.get("voice_url")
		session["image_prompt"] = image_prompt
		session["video_prompt"] = video_prompt
		session["speech_prompt"] = speech_prompt
		session["language"] = language
		if image_prompt and video_prompt and speech_prompt:
			image = Image(image_prompt)
			video = Video(video_prompt)
			if not language:
				language = "English Text (eng)"
			if voice_file or (voice_file and voice_url):
				voice_file.save(os.path.join(app.config['uploadFolder'], voice_file.filename))
				speech = Speech(speech_prompt, voice_file.filename, language)
			elif voice_url:
				speech = Speech(speech_prompt, voice_url, language)
			else:
				speech = Speech(speech_prompt, language)
		else:
			flash("Must fill in all the prompts")
			return render_template("home.html")
		session["image"] = image
		session["video"] = video
		session["speech"] = speech
		return render_template("results.html", image=image, video=video, speech=speech)
	else:
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
	if change_image:
		image = Image(session["image_prompt"], True)
		return render_template("results.html", image=image, video=session["video"], speech=session["speech"])
	elif change_audio:
		speech = Speech(session["speech_prompt"], session["language"], True)
		return render_template("results.html", speech=speech, video=session["video"], image=session["image"])
	else:
		video = Video(session["video_prompt"], True)
		return render_template("results.html", image=session["image"], video=video, speech=session["speech"])
	
