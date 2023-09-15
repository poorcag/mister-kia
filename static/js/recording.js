const recordButton = document.getElementById('recordButton');

const rec_state = {
    AWAITING : 0,
    RECORDING : 1,
    RESPONDING : 2
}

let cur_state = rec_state.AWAITING
let isResponding = false
let chatContext = []
let mediaRecorder;

recordButton.addEventListener('click', () => {
    if (cur_state == rec_state.AWAITING) {
        // startRecording();
    } else if (cur_state == rec_state.RECORDING) {
        stopRecording();
    } else if (cur_state == rec_state.RESPONDING) {
        
    }
});

function setButtonState(new_state) {
    if (new_state == rec_state.AWAITING) {
        recordButton.textContent = "Tap and ask"
    }
    else if (new_state == rec_state.RECORDING) {
        recordButton.textContent = "Tap again when done"
        recordButton.classList.add('recording-on');
    }
    else if (new_state == rec_state.RESPONDING) {
        recordButton.textContent = "Responding now"
        recordButton.classList.remove('recording-on');
    }
    cur_state = new_state
}

document.querySelector('.microphone-button').addEventListener('mousedown', (evt) => {
    evt.target.classList.add('loading')

    setTimeout(() => {
        evt.target.classList.remove('loading')
    }, 3000);
})

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

const startRecording = async () => {
    setButtonState(rec_state.RECORDING)
    chunks = [];
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/mp3' });
        const url = URL.createObjectURL(blob);
        console.log(url);

        const formData = new FormData()
        formData.append("audio_file", blob)

        const headers = new Headers();
        headers.append('chat_context', JSON.stringify(chatContext));
        console.log(chatContext)

        fetch("https://mister-kia-qrbozmensq-km.a.run.app/upload_audio/", {
            method: 'POST',
            body: formData,
            headers: headers
        })
            .then(response => {
                console.log("Response from server:", response);
                chatContext.push(response.headers.get('transcription'))
                chatContext.push(response.headers.get('answer'))
                console.log(chatContext)
                response.blob().then((blob) => {
                    const objectURL = URL.createObjectURL(blob);
                    const audioElement = new Audio();
                    audioElement.addEventListener("ended", () => { setButtonState(rec_state.AWAITING); }, false);
                    audioElement.src = objectURL;
                    audioElement.play();
                }).catch(error => {
                    console.error("Error from the blob:", error);
                    setButtonState(rec_state.AWAITING);
                })
            })
            .catch(error => {
                console.error("Error from the server:", error);
                setButtonState(rec_state.AWAITING);
            })

        await sleep(1500);

        var idx = getRandomInt(2)

        var audio_elem_id = "audio-thinking-" + idx
        console.log(audio_elem_id)
        console.log(idx)

        var thinkingAudio = document.getElementById(audio_elem_id);
        thinkingAudio.play()
    };
    mediaRecorder.start();
};

const stopRecording = () => {
    setButtonState(rec_state.RESPONDING);
    console.log("stopping recording")
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }
};

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function (stream) {
        console.log('You let me use your mic!')
    })
    .catch(function (err) {
        console.log('No mic for you!')
    });