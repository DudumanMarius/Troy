$(document).ready(function() {
    const listenBtn = $("#listenBtn");
    const stopBtn = $("#stopBtn");
    const transText = $('#transcribedText');
    let mediaRecorder = null;
    let socket = null;

    function setupWebSocket(stream) {
        if (!MediaRecorder.isTypeSupported('audio/webm'))
            return alert('Browser not supported');

        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm',
        })

        socket = new WebSocket('ws://localhost:8000/listen');

        socket.onopen = () => {
            console.log({ event: 'onopen' });
            mediaRecorder.addEventListener('dataavailable', async (event) => {
                if (event.data.size > 0 && socket.readyState == 1) {
                    socket.send(event.data);
                }
            })
            mediaRecorder.start(250);
            listenBtn.prop("disabled", true)
            stopBtn.prop("disabled", false);
            const now = new Date();
            const current = now.getHours() + ':' + now.getMinutes();
            $("#liveToast").toast('show');
            $("#toastTime").text(current);
            $("#toastText").text("Listening is ON right now.");
        }

        socket.onmessage = (message) => {
            const received = message.data;
            if (received) {
                transText.val(transText.val() + " " + received);
            }
        }

        socket.onclose = () => {
            console.log({ event: 'onclose' });
            stopBtn.prop("disabled", true)
            listenBtn.prop("disabled", false);
            const now = new Date();
            const current = now.getHours() + ':' + now.getMinutes();
            $("#liveToast").toast('show');
            $("#toastTime").text(current);
            $("#toastText").text("Listening is OFF right now.")
        }

        socket.onerror = (error) => {
            console.log({ event: 'onerror', error });
        }
    }

    listenBtn.on("click", function () {
        navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => setupWebSocket(stream));
    });

    stopBtn.on("click", function () {
        mediaRecorder.stop(250);
        socket.close();
    });
});