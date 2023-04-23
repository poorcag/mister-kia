# import whisper

# model = whisper.load_model("small")
# result = model.transcribe("input.mp3")
# print(result["text"])

import os
import openai

openai.api_key_path = '.key'

async def transcribe_from_audio(audio_blob):
    print (audio_blob)
    audio = openai.Audio(audio_blob.file)
    transcript = openai.Audio.transcribe("whisper-1", audio)

    return transcript

# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ]
# )
# print(response)

# with open("input.mp3", "rb") as audio_file:
#     transcript = openai.Audio.transcribe("whisper-1", audio_file)
#     print(transcript)