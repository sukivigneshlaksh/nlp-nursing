import whisper
import pyaudio
import tempfile
import wave
import os

class SimpleWhisperStreamer:
    def __init__(self):
        self.model = whisper.load_model("base")
        self.audio = pyaudio.PyAudio()
        
    def record_and_transcribe(self, duration=5):
        """Record audio for specified duration and return transcription."""
        # Record audio
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        print(f"Recording for {duration} seconds...")
        frames = []
        for _ in range(0, int(16000 / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        
        # Save as temporary WAV file
        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                with wave.open(temp_file.name, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(16000)
                    wf.writeframes(b''.join(frames))
                
                # Transcribe with Whisper
                result = self.model.transcribe(temp_file.name, fp16=False)
                return result['text'].strip()
        finally:
            # Clean up temp file
            if temp_file and os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    
    def cleanup(self):
        self.audio.terminate()

if __name__ == "__main__":
    streamer = SimpleWhisperStreamer()
    try:
        text = streamer.record_and_transcribe(duration=5)
        print(f"Transcription: {text}")
    finally:
        streamer.cleanup()