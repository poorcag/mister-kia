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

    tf = tempfile.NamedTemporaryFile(suffix='.mp3')
    output_file = tf.name

    # TODO - figure out how to do this without having to manually save the file
    contents = audio_file.file.read()
    async with aiofiles.open(output_file, 'wb') as f:
        await f.write(contents)

    transcript = ''
    async with aiofiles.open(output_file, "rb") as f:
        
        data = await f.read()

        transcript = await openai.Audio.atranscribe_raw("whisper-1", data, output_file)

    print (transcript)

    return {
        "filename" : output_file,
        "transcription": transcript 
    }