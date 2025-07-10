document.addEventListener('DOMContentLoaded', function() {
    const recordBtn = document.getElementById('record-btn');
    const stopBtn = document.getElementById('stop-btn');
    const statusEl = document.getElementById('recording-status');
    const voicePitchInput = document.getElementById('voice_pitch');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        let mediaRecorder;
        let audioChunks = [];

        recordBtn.addEventListener('click', () => {
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    mediaRecorder = new MediaRecorder(stream);
                    mediaRecorder.start();

                    statusEl.textContent = 'Recording...';
                    recordBtn.disabled = true;
                    stopBtn.disabled = false;

                    mediaRecorder.addEventListener('dataavailable', event => {
                        audioChunks.push(event.data);
                    });

                    mediaRecorder.addEventListener('stop', () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                        const audioFile = new File([audioBlob], "voice_pitch.mp3", { type: 'audio/mpeg' });
                        
                       
                        const dataTransfer = new DataTransfer();
                        dataTransfer.items.add(audioFile);
                        voicePitchInput.files = dataTransfer.files;

                        statusEl.textContent = 'Recording complete. File is attached.';
                        recordBtn.disabled = false;
                        stopBtn.disabled = true;
                        audioChunks = [];
                    });
                })
                .catch(err => {
                    console.error("Error accessing microphone:", err);
                    statusEl.textContent = 'Microphone access denied.';
                });
        });

        stopBtn.addEventListener('click', () => {
            mediaRecorder.stop();
        });

    } else {
        document.getElementById('recorder-ui').innerHTML = '<p class="text-muted small">Audio recording not supported in your browser.</p>';
    }
});