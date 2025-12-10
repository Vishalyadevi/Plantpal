// Voice Input using Web Speech API

document.addEventListener('DOMContentLoaded', function() {
    const voiceBtn = document.getElementById('voiceBtn');
    const moodText = document.getElementById('moodText');
    
    if (!voiceBtn || !moodText) return;
    
    // Check if browser supports speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        voiceBtn.style.display = 'none';
        console.log('Speech recognition not supported in this browser');
        return;
    }
    
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    
    let isRecording = false;
    
    voiceBtn.addEventListener('click', function() {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    });
    
    function startRecording() {
        try {
            recognition.start();
            isRecording = true;
            voiceBtn.classList.add('recording');
            voiceBtn.innerHTML = '<i class="bi bi-mic-mute-fill"></i>';
            voiceBtn.title = 'Stop recording';
            
            // Add visual feedback
            moodText.style.borderColor = '#ef4444';
            moodText.placeholder = 'Listening... Speak now!';
        } catch (error) {
            console.error('Error starting recognition:', error);
            showError('Could not start voice recording. Please try again.');
        }
    }
    
    function stopRecording() {
        recognition.stop();
        isRecording = false;
        voiceBtn.classList.remove('recording');
        voiceBtn.innerHTML = '<i class="bi bi-mic-fill"></i>';
        voiceBtn.title = 'Start recording';
        
        // Reset visual feedback
        moodText.style.borderColor = '';
        moodText.placeholder = 'Type or speak your feelings...';
    }
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        
        // Append to existing text or replace if empty
        if (moodText.value.trim()) {
            moodText.value += ' ' + transcript;
        } else {
            moodText.value = transcript;
        }
        
        // Trigger input event for any listeners
        moodText.dispatchEvent(new Event('input'));
        
        // Show success feedback
        showSuccess('Voice input captured successfully!');
        stopRecording();
    };
    
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        stopRecording();
        
        let errorMessage = 'Voice input failed. Please try again.';
        
        switch(event.error) {
            case 'no-speech':
                errorMessage = 'No speech detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage = 'No microphone found. Please check your device.';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone permission denied. Please allow access.';
                break;
            case 'network':
                errorMessage = 'Network error. Please check your connection.';
                break;
        }
        
        showError(errorMessage);
    };
    
    recognition.onend = function() {
        if (isRecording) {
            stopRecording();
        }
    };
    
    // Helper functions for feedback
    function showSuccess(message) {
        const alert = createAlert(message, 'success');
        insertAlert(alert);
    }
    
    function showError(message) {
        const alert = createAlert(message, 'danger');
        insertAlert(alert);
    }
    
    function createAlert(message, type) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.style.position = 'fixed';
        alert.style.top = '20px';
        alert.style.right = '20px';
        alert.style.zIndex = '9999';
        alert.style.minWidth = '300px';
        alert.style.animation = 'slideInRight 0.3s ease';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        return alert;
    }
    
    function insertAlert(alert) {
        document.body.appendChild(alert);
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 3000);
    }
    
    // Add animation keyframes
    if (!document.querySelector('#voiceAnimations')) {
        const style = document.createElement('style');
        style.id = 'voiceAnimations';
        style.textContent = `
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
        `;
        document.head.appendChild(style);
    }
});