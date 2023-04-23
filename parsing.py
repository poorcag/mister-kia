# import whisper

# model = whisper.load_model("small")
# result = model.transcribe("input.mp3")
# print(result["text"])

import openai

openai.api_key_path = '.key'

async def transcribe_from_audio(audio_file):

    contents = audio_file.file.read()
    transcript = await openai.Audio.atranscribe_raw("whisper-1", contents, f"{audio_file.filename}.mp3")

    body_text = transcript.get('text', '')

    return body_text

async def answer_my_question(question_text):

    print(question_text)

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful kindergarden teacher."},
                {"role": "user", "content": "I'd like to ask you a question. Please keep your answer short, simple, and accurate. Answer like you're talking to a primary school student."},
                {"role": "assistant", "content": "Of course, ask me anything you'd like!"},
                {"role": "user", "content": question_text}
            ]
        )
    print(response)

    output_message = response.get('choices')[0].get('message').get('content')

    return output_message
