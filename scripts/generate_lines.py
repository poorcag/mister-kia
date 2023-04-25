from elevenlabs import set_api_key, generate, save

with open('../.elevenapikey') as f:
    set_api_key(f.read())

def make_file(text):
    audio = generate(text, voice='Sam')
    save(audio, f"{text.replace(' ', '_')}.mp3")