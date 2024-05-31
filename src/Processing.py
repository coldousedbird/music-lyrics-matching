from datetime import datetime

import speech_recognition as sr
from pydub import AudioSegment
import librosa
# import torch
# from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import concurrent.futures
from io import BytesIO
import syncedlyrics

class Processing:
    def __init__(self):
        self.song_path = None
        self.song = None

        self.lyrics_path = None
        self.lyrics = None

        self.request_time = None
        self.result = None
        

    # Разбиение аудио на сегменты по 5 секунд
    def process_segment(self, i):
        segment = self.audio[i:i+5000]
        # Инициализация распознавателя речи
        r = sr.Recognizer()
        with BytesIO() as bio:
            segment.export(bio, format="wav")
            bio.seek(0)
            try:
                # Распознавание текста в сегменте
                with sr.AudioFile(bio) as source:
                    audio_data = r.record(source)
                    text = r.recognize_google(audio_data, language="en-US")
                    start_time = i / 1000  # Время начала сегмента в секундах
                    end_time = (i + 5000) / 1000  # Время окончания сегмента в секундах
                    return (start_time, end_time, text)
            except (sr.UnknownValueError, FileNotFoundError):
                return None

    def process(self):
        # NOW IT IS JUST LOADING LRC FROM INTERNET. LATER, IT'LL USE MODEL 
        # LATER HERE MUST BE MODEL, WHICH WILL PROCESS FILES THROUGH
        # print("process started")
        try:
            self.request_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.result = syncedlyrics.search(self.song_path[0:-4], providers=["Lrclib", "NetEase", "Megalobiz"])
        except Exception as e:
            print(e, "\" occured, skipping track -")

        # self.request_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        # # Загрузка аудио файла
        # song_path = "temp/processed_song.mp3"
        # with open(song_path, "wb") as song:
        #     song.write(self.song)
        
        # self.audio = AudioSegment.from_file(song_path, format="mp3")
        # self.audio = self.audio.normalize()

        # # Улучшение качества аудио
        # #audio_data = self.audio.raw_data         # ???

        # # Шумоподавление
        # self.audio = self.audio.apply_gain(-20.0)  # Применение шумоподавления
        # self.audio = self.audio.normalize()  # Нормализация аудио


        # # # Загрузка предварительно обученной модели (кэширование)
        # # model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        # # tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")

        # # Создание списка для хранения результатов распознавания
        # results = []

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     for result in executor.map(self.process_segment, range(0, len(self.audio), 5000)):
        #         if result:
        #             results.append(result)

        # # Сортировка результатов по времени начала
        # results.sort(key=lambda x: x[0])

        # # Вывод результатов распознавания с временными метками
        # for start_time, end_time, text in results:
        #     minutes = int(start_time // 60)
        #     seconds = start_time % 60
        #     print(f"[{minutes:02d}:{seconds:05.2f}] {text}")


        
