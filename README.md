# Description
This project aims to streamline the creation process for creators, allowing many to create a whole product with just a drop of inspiration. With our website, users can create a full-fledged video with just their ideas expressed in textual form, providing a safe haven for non-artistically inclined creators (includes skills like directing, video editing, etc). 

For example, with just a prompt and the click of a button, users can generate a thumbnail (image), content (video), a narrator (audio) and background audio all at once to post on their desired platform. Furthermore, we allow easy customisation and provide choices, so users are not stuck with only one option that does not fit their requirements.

## Problem Statement
In the scenarios of creating and consuming streaming media content, generative Al technologies
can be utilized for content optimization, information extraction, and style transformation, to
refine content across various media platforms. With these technologies, we can cater to the
preferences of diverse audiences, as well as facilitate creators in producing higher quality
content more efficiently.

# Features and Functionality

## Content Generation
- Image generation with prompt (Optional parameter: negative prompt)
- Video generation with prompt
- Speech generation with prompt (Optional parameters: language, gender of speaker, voice source)
- Sound Effect Generation with prompt

### Additional functionality
- Change generated content if not satisfied with the current one 
    - Speech has limited options so it will switch back to the original one eventually
- Combine generated content into a final video
    - Can input own media files to combine as well

# Tools used
1. GitHub
2. VS Code
3. Bootstrap v5.0.2
4. HuggingFace

## APIs used
- HuggingFace Spaces gradio API
    1. Aqcua/TextToImage-AISDXLTURBO
    2. stabilityai/stable-diffusion-3-medium
    3. tonyassi/voice-clone
    4. k2-fsa/text-to-speech
    5. BestWishYsh/MagicTime
    6. https://videocrafter-videocrafter.hf.space/
    7. https://haoheliu-audioldm2-text2audio-text2music.hf.space/
    8. eagle0504/stable-audio-demo

## Assets used
<p float="left">
  <img src="/static/assets/error.png" height="200" />
  <img src="/static/assets/one.png" height="200" /> 
  <img src="/static/assets/two.png" height="200" />
</p>


## Python Libraries used
- flask and flask_session
- os
- time
- gradio_client
- requests
- json
- shutil
- random
- moviepy
- cv2
- PIL
- ffmpeg

# Using Content Generator
1. Go into the root folder
```bash
cd TikTok-TechJam-main
```
2. Activate the virtual environment
```bash
source venv/bin/activate
```
3. Install packages in requirements.txt
```bash
pip install -r requirements.txt
```
4. Start server
```bash
gunicorn -w 4 -b 0.0.0.0 'app:create_app()' --timeout 500
```
