# Content Generator
# Description
This project aims to streamline the creation process for creators, allowing many to create a whole product with just a drop of inspiration. With our website, users can create a full-fledged video with just their ideas expressed in textual form, providing a safe haven for creators who are not artistically inclined (includes skills like directing, video editing, etc). 

For example, with just a prompt, users can generate a thumbnail (image), content (video), and a narrator (audio) all at once. Furthermore, we allow easy customisation and provide choices, so users are not stuck with only one option that does not fit their needs.

## Problem Statement
In the scenarios of creating and consuming streaming media content, generative Al technologies
can be utilized for content optimization, information extraction, and style transformation, to
refine content across various media platforms. With these technologies, we can cater to the
preferences of diverse audiences, as well as facilitate creators in producing higher quality
content more efficiently.

# Features and Functionality

## Content Generation
- Image generation with prompt (and negative prompt)
- Video generation with prompt
- Speech generation with prompt (Optional parameters: language, gender of speaker, voice source)
(- Generating sound effects)

### Additional functionality
- Button to change generated content if not satisfied with current one 
    - Speech has limited options so it will switch back to original one eventually

## Gaining Insights From Media Content
- Identifying text in image
- Summarising YouTube videos

# Tools used
1. GitHub
2. VS Code
3. HuggingFace

## APIs used
- HuggingFace Spaces gradio API
    1. Aqcua/TextToImage-AISDXLTURBO
    2. stabilityai/stable-diffusion-3-medium
    3. tonyassi/voice-clone
    4. k2-fsa/text-to-speech
    5. BestWishYsh/MagicTime
    6. https://videocrafter-videocrafter.hf.space/
    7. gokaygokay/Florence-2
    8. https://sudarshanar-videosummaryfromyoutubevideo.hf.space/api/predict
(    9. https://haoheliu-audioldm2-text2audio-text2music.hf.space/)

## Assets used

## Libraries used
- flask and flask_session
- os
- time
- threading
- gradio_client
- requests
- json
- shutil



