from gradio_client import Client, handle_file

import requests
client = Client("Flux9665/MassivelyMultilingualTTS")
result = client.predict(
		prompt="hello",
		language="English Text (eng)",
		voice_seed=279,
		duration_scaling_factor=1,
		pitch_variance_scale=1,
		energy_variance_scale=1,
		emb1=0,
		emb2=0,
		api_name="/predict"
)	
print(result)