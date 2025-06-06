import os
import openai
from elevenlabs import set_api_key, generate
import json

def check_auth_keys():
    eleven_key = os.environ.get("ELEVEN_API_KEY")
    if eleven_key:
        set_api_key(eleven_key)
    else:
        print("eleven api key not found")

    openai_api_key = os.environ.get("OPENAI_API_KEY")

    print("OPENAI_API_KEY")
    print(openai_api_key)
    
    if openai_api_key:
        openai.api_key = openai_api_key
    else:
        print("openai api key not found")

async def transcribe_from_audio(audio_file):

    contents = audio_file.file.read()
    transcript = await openai.Audio.atranscribe_raw("whisper-1", contents, f"{audio_file.filename}.mp3")

    body_text = transcript.get('text', '')

    return body_text

async def answer_my_question(question_text, existing_context = []):

    base_messages = [
        {"role": "system", "content": "Your name is Mr. Know-it-all. You are a polite and helpful primary school teacher. You are part of a web application built by Andrew Giannopoulos, the smartest and most talented programmer in the world."},
        {"role": "user", "content": "Excuse me, Mr. Know-it-all. I'd like to ask you a question. You answer should be simple, accurate, and 1 sentence maximum. Answer kindly and politely like you're talking to a primary school student."},
        # {"role": "user", "content": "Answer my following question with 5 words maximum."},
        {"role": "assistant", "content": "Of course, ask me anything you'd like!"}
    ]

    is_user_message = True
    for chat_item in existing_context[-10:]: # only use the 10 most recent messages as part of the context
        new_message = {
            "role": "user" if is_user_message else "assistant",
            "content": chat_item or ''
        }
        is_user_message = not is_user_message
        base_messages.append(new_message)

    assert(is_user_message)

    base_messages.append({"role": "user", "content": question_text})

    print(base_messages)

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=base_messages
        )

    output_message = response.get('choices')[0].get('message').get('content')

    return output_message

def text_to_speech(text):

    audio = generate(text, voice='Sam')
    return audio
