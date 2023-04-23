from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from parsing import transcribe_from_audio

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

import openai

openai.api_key_path = '.key'

@app.post("/upload_audio/")
async def upload_audio_file(audio_file: UploadFile = File(...)):
    print(audio_file.filename)
    print(audio_file.content_type)
    print(audio_file.size)

    filename = f"{audio_file.filename}.mp3"

    # TODO - figure out how to do this without having to manually save the file
    contents = audio_file.file.read()
    with open(filename, 'wb') as f:
        f.write(contents)

    import subprocess, tempfile, uuid

    # tf = tempfile.NamedTemporaryFile(suffix='.mp3')
    # output_file = tf.name

    # output_file = f"{uuid.uuid4()}.mp3"

    # print(subprocess.run(f'ffmpeg -i {audio_file.filename} -acodec libmp3lame {output_file}',shell=True,capture_output=True))

    # transcript = await transcribe_from_audio(audio_file)

    # print (transcript)
    
    transcript = ''
    with open(filename, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)

    print (transcript)

    return {
        "filename" : audio_file.filename,
        "transcription": transcript 
    }