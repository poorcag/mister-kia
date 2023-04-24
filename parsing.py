# import whisper

# model = whisper.load_model("small")
# result = model.transcribe("input.mp3")
# print(result["text"])

import openai
from elevenlabs import set_api_key, generate

openai.api_key_path = '.key'

eleven_api_key = ''
with open('.elevenapikey') as f:
    eleven_api_key = f.read()

set_api_key(eleven_api_key)

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
                {"role": "system", "content": "You are a helpful primary school teacher."},
                # {"role": "user", "content": "I'd like to ask you a question. You answer should be simple, accurate, and 2 sentences maximum. Answer kindly and politely like you're talking to a primary school student."},
                {"role": "user", "content": "Answer my following question with 5 words maximum."},
                {"role": "assistant", "content": "Of course, ask me anything you'd like!"},
                {"role": "user", "content": question_text}
            ]
        )
    print(response)

    output_message = response.get('choices')[0].get('message').get('content')

    return output_message


def text_to_speech(text):

    print (text)
    audio = generate(text)
    return audio
