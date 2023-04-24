from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse

from src.parsing import transcribe_from_audio, answer_my_question, text_to_speech

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
    return {"Hello": "Everybody"}

@app.post("/upload_audio/")
async def upload_audio_file(audio_file: UploadFile = File(...)):
    print(audio_file.filename)
    print(audio_file.content_type)
    print(audio_file.size)

    transcript = await transcribe_from_audio(audio_file)

    answer = await answer_my_question(transcript)

    answer_audio = text_to_speech(answer)

    # create a dictionary with the response data
    response_data = {
        "filename" : audio_file.filename,
        "transcription": transcript,
        "answer": answer,
        "file_size": len(answer_audio)
    }

    # create a response object with the audio file and the response data
    response = Response(content=answer_audio, media_type="audio/mp3", status_code=200)
    response.headers["Content-Disposition"] = "attachment; filename=audio.mp3"
    response.headers["filename"] = audio_file.filename
    response.headers["transcription"] = transcript
    response.headers["answer"] = answer
    response.headers["file_size"] = str(len(answer_audio))
    return response