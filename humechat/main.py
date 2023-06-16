import threading
import asyncio
import os
import cv2
import time
import traceback
import websockets
import numpy as np

from pynput import keyboard
from pvrecorder import PvRecorder
from whispercpp import Whisper
from chat import message, store_emotions
from playsound import playsound
from hume import HumeStreamClient, HumeClientException
from hume.models.config import FaceConfig
from gtts import gTTS

# Configurations
HUME_API_KEY = ""
HUME_FACE_FPS = 1 / 3  # 3 FPS

TEMP_FILE = 'temp.jpg'
TEMP_WAV_FILE = 'temp.wav'

# Initialize whisper model, pyttsx3 engine, and pv recorder
w = Whisper.from_pretrained("tiny.en")
recorder = PvRecorder(device_index=-1, frame_length=512)

# Global variables
recording = False
recording_data = []

# Webcam setup
cam = cv2.VideoCapture(0)


async def webcam_loop():
    while True:
        try:
            client = HumeStreamClient(HUME_API_KEY)
            config = FaceConfig(identify_faces=True)
            async with client.connect([config]) as socket:
                print("(Connected to Hume API!)")
                while True:
                    if not recording:
                        _, frame = cam.read()
                        cv2.imwrite(TEMP_FILE, frame)
                        result = await socket.send_file(TEMP_FILE)
                        store_emotions(result)
                        await asyncio.sleep(1 / 3)
        except websockets.exceptions.ConnectionClosedError:
            print("Connection lost. Attempting to reconnect in 1 seconds.")
            time.sleep(1)
        except HumeClientException:
            print(traceback.format_exc())
            break
        except Exception:
            print(traceback.format_exc())


def start_asyncio_event_loop(loop, asyncio_function):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio_function)


def recording_loop():
    global recording_data, recording
    while recording:
        frame = recorder.read()
        recording_data.append(frame)

    recorder.stop()
    print("(Recording stopped...)")

    recording_data = np.hstack(recording_data).astype(np.int16).flatten().astype(np.float32) / 32768.0
    transcription = w.transcribe(recording_data)
    response = message(transcription)
    tts = gTTS(text=response, lang='en')
    tts.save(TEMP_WAV_FILE)
    playsound(TEMP_WAV_FILE)
    os.remove(TEMP_WAV_FILE)


def on_press(key):
    global recording, recording_data, recorder
    if key == keyboard.Key.space:
        if recording:
            recording = False
        else:
            recording = True
            recording_data = []
            recorder.start()
            print("(Recording started...)")
            threading.Thread(target=recording_loop).start()


new_loop = asyncio.new_event_loop()

threading.Thread(target=start_asyncio_event_loop, args=(new_loop, webcam_loop())).start()

with keyboard.Listener(on_press=on_press) as listener:
    print("Speak to Joaquin!")
    print("(Press spacebar to speak. To finish speaking, press spacebar again)")
    listener.join()
