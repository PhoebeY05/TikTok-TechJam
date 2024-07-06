from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import ffmpeg

content_folder = 'static/content'

def sound_effect_trim(sound_effect, duration):
	audio_input = ffmpeg.input(sound_effect)
	audio_cut = audio_input.audio.filter('atrim', duration=duration)
	audio_output = ffmpeg.output(audio_cut, os.path.join(content_folder, "trim_effect.mp3"))
	ffmpeg.run(audio_output)
	
def audio_trim(video, audio, sound_effect):
	# Trimming audio files to fit video's duration
	duration = video.duration
	# Speech
	audio_input = ffmpeg.input(audio)
	audio_cut = audio_input.audio.filter('atrim', duration=duration)
	audio_output = ffmpeg.output(audio_cut, os.path.join(content_folder, "trim_speech.mp3"))
	ffmpeg.run(audio_output)
	# Sound effect
	if sound_effect:
		sound_effect_trim(sound_effect, duration)
	return os.path.join(content_folder, "trim_speech.mp3")

def video_trim(video, audio, sound_effect):
	# Trimming video and sound_effect files to fit audio's duration
	duration = audio.duration
	ffmpeg_extract_subclip(video, 0, duration, targetname=os.path.join(content_folder, "trim_video.mp4"))
	if sound_effect:
		sound_effect_trim(sound_effect, duration)
	return os.path.join(content_folder, "trim_video.mp4")