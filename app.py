from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
import openai
import tempfile

from parsing import transcribe_from_audio

openai.api_key_path = '.key'

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"Hello": "world"}

@app.post("/upload_audio/")
async def upload_audio_file(audio_file: UploadFile = File(...)):
    print(audio_file.filename)
    print(audio_file.content_type)
    print(audio_file.size)

    contents = audio_file.file.read()
    transcript = await openai.Audio.atranscribe_raw("whisper-1", contents, f"{audio_file.filename}.mp3")

    print (transcript)

    return {
        "filename" : audio_file.filename,
        "transcription": transcript 
    }