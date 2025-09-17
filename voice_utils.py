import speech_recognition as sr
import pyttsx3
import threading

# 🎤 Speech to Text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Error: Speech Recognition service unavailable."
    except Exception as e:
        return f"Unexpected error: {e}"

# 🔊 Text to Speech (non-blocking with threading)
def text_to_speech(text):
    def run_tts():
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {e}")

    tts_thread = threading.Thread(target=run_tts)
    tts_thread.start()
