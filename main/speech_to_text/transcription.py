import io
import os
import pyaudio
from google.cloud import speech
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_CLOUD_CREDENTIALS")


# Audio stream settings
RATE = 16000  
CHUNK = int(RATE / 10) 


def capture_audio():
    """
    Capture audio from the microphone in real time.
    This function opens an audio stream using the PyAudio library and captures audio data in chunks.
    It yields each chunk of audio data as it is captured. The function runs indefinitely until a 
    KeyboardInterrupt is received, at which point it stops the audio stream and terminates the 
    audio interface.
    Yields:
        bytes: A chunk of audio data captured from the microphone.
    """    
   
    audio_interface = pyaudio.PyAudio()

    stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Listening...")
    try:
        for _ in iter(int, 1):
            yield stream.read(CHUNK)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()


def transcribe_streaming():
    """
    Stream audio to Google Speech-to-Text API for real-time transcription.
    This function captures audio in real-time, streams it to the Google Speech-to-Text API,
    and processes the responses to extract the transcribed text and its confidence score.
    Returns:
        tuple: A tuple containing the transcribed text (str) and the confidence score (float).
    """

    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(config=config)

    # Create request generator
    def request_generator():
        for content in capture_audio():
            yield speech.StreamingRecognizeRequest(audio_content=content)

    responses = client.streaming_recognize(streaming_config, request_generator())

    # Process the responses
    for response in responses:
        for result in response.results:
            return result.alternatives[0].transcript, result.alternatives[0].confidence


if __name__ == "__main__":
    transcribe_streaming()
