import os
import openai
import whisper
import ffmpeg
import random
import wave
import time
import threading
import tkinter as tk
import pyaudio

API_KEY = 'API_KEY'
os.environ['OPENAI_Key'] = API_KEY
openai.api_key = os.environ['OPENAI_Key']


class VoiceRecorder:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.button = tk.Button(text="Record", 
                                font=("Arial", 120, "bold"),
                                command=self.click_handler)
        self.button.pack()
        self.label = tk.Label(text="00:00:00")
        self.label.pack()
        self.recording = False
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1, rate=44100,
                            input=True,
                            frames_per_buffer=1024)
        frames = []
        start = time.time()
        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        stream.stop_stream()
        stream.close()

        exists = True
        i = 1
        while exists:
            if os.path.exists(f"input{i}.wav"):
                i += 1
            else:
                exists = False
        sound_file = wave.open(f"input{i}.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()


def transcribe(audio):
    model = whisper.load_model("base")

    audio = whisper.load_audio(audio)

    result = model.transcribe(audio, fp16=False)

    return result['text']


def chatbot():
    scenarios = ["a patient with symptoms of the flu that have been developing over the past week during a doctor examination.",
                 "a patient with chronic high blood pressure during a doctor examination.",
                 "a patient with a wrist that was broken in a soccer game during a doctor examination.",
                 "a patient who has been suffering from depression for the past year during an examination with their doctor",
                 "a patient during their post-surgery follow-up with their doctor after their successful hip surgery"]

    keep_prompting = True
    scenario = random.randint(0, 4)
    while keep_prompting:
        VoiceRecorder()

        exists = True
        i = 1
        while exists:
            if os.path.exists(f"input{i+1}.wav"):
                i += 1
            else:
                exists = False
        user_input = transcribe(f"./input{i}.wav")

        if user_input == 'complete':
            keep_prompting = False
        else:
            response = openai.Completion.create(
                model="text-curie-001",
                prompt=user_input + 'Please respond as if you are ' + scenarios[scenario],
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print(response["choices"][0]["text"].strip())


def main():
    chatbot()


if __name__ == "__main__":
    main()
