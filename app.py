from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from parsing import transcribe_from_audio, answer_my_question

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

    transcript = await transcribe_from_audio(audio_file)

    answer = await answer_my_question(transcript)

    return {
        "filename" : audio_file.filename,
        "transcription": transcript,
        "answer": answer
    }