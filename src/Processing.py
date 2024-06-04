from datetime import datetime
import syncedlyrics
from pydub import AudioSegment
import numpy as np

import speech_recognition as sr
import concurrent.futures
from io import BytesIO

# for test_Processing
from sys import argv
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog

# import librosa
# import torch
# from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer


class Processing:
    def __init__(self) -> None:
        self.song_name = None
        self.song = None

        self.lyrics_name = None
        self.lyrics = None

        self.request_time = None
        self.result = None
        
    def extract_name_from_path(self, path: str) -> str:
        file = path.rsplit("/", 1)
        return file[-1][:-4] if len(path) > 1 else path[:-4]

    def load_song(self, path: str) -> None:
        self.song_name = self.extract_name_from_path(path)
        with open(path, 'rb') as song:
            self.song = song.read()

    def load_lyrics(self, path: str) -> None:
        self.lyrics_name = self.extract_name_from_path(path)
        with open(path, 'r') as lyrics:
            self.lyrics = lyrics.read()

    def find(self) -> None:
        try:
            self.request_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.result = syncedlyrics.search(self.song_name, providers=["Lrclib", "NetEase", "Megalobiz"])
        except Exception as e:
            print(e, "\" occured, skipping track -")

    def recognize(self) -> None:
        # # Загрузка аудиозаписи
        # audio = AudioSegment.from_file("input.mp3", format="mp3")

        # # Очистка аудиозаписи от шумов
        # denoised_audio = audio.apply_gain(-20.0)

        # # Разделение аудиозаписи на отдельные фрагменты с вокалом
        # threshold = -30  # Порог для определения наличия вокала
        # segments = []
        # current_segment = None
        # for i, sample in enumerate(denoised_audio.raw_data):
        #     if abs(sample) > threshold:
        #         if current_segment is None:
        #             current_segment = denoised_audio[i:i+1]
        #     else:
        #         if current_segment is not None:
        #             segments.append(current_segment)
        #             current_segment = None
        # if current_segment is not None:
        #     segments.append(current_segment)

        # # Сохранение очищенной аудиозаписи и отдельных фрагментов
        # denoised_audio.export("output.mp3", format="mp3")
        # for i, segment in enumerate(segments):
        #     segment.export(f"segment_{i+1}.mp3", format="mp3")


        self.request_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        # Загрузка аудио файла
        song_path = "temp/processed_song.mp3"
        with open(song_path, "wb") as song:
            song.write(self.song)
        
        self.audio = AudioSegment.from_file(song_path, format="mp3")
        self.audio = self.audio.normalize()

        # Улучшение качества аудио
        #audio_data = self.audio.raw_data         # ???

        # Шумоподавление
        self.audio = self.audio.apply_gain(-20.0)  # Применение шумоподавления
        self.audio = self.audio.normalize()  # Нормализация аудио


        # # Загрузка предварительно обученной модели (кэширование)
        # model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        # tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")

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

        # Создание списка для хранения результатов распознавания
        results = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for result in executor.map(process_segment, range(0, len(self.audio), 5000)):
                if result:
                    results.append(result)

        # Сортировка результатов по времени начала
        results.sort(key=lambda x: x[0])

        # Вывод результатов распознавания с временными метками
        for start_time, end_time, text in results:
            minutes = int(start_time // 60)
            seconds = start_time % 60
            print(f"[{minutes:02d}:{seconds:05.2f}] {text}")

        return ""

# test function for Processing class
def test_Processing() -> None:
    app = QApplication(argv)
    window = QWidget()
    window.show()

    p = Processing()
    file_dialog = QFileDialog(window)
    file_dialog.setNameFilter("Audio files (*.mp3 *.wav)")

    if file_dialog.exec():
        path = file_dialog.selectedFiles()[0]
        p.load_song(path)
        print(f"selected song: {p.song_name}")
        print(f"type of song: {type(p.song)}")

    file_dialog.setNameFilter("Text files (*.txt)")
    if file_dialog.exec():
        path = file_dialog.selectedFiles()[0]
        p.load_lyrics(path)
        print(f"selected lyrics: {p.lyrics_name}")

    # result = p.process

    exit(app.exec())


if __name__ == "__main__":
    test_Processing()