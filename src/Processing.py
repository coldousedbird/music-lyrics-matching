from datetime import datetime
from time import time
import syncedlyrics
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import whisper


class Processing:
    def __init__(self) -> None:
        self.song_path = None
        self.song_name = None
        self.song = None
        self.audio = None
        self.rate = None

        self.lyrics_path = None
        self.lyrics_name = None
        self.lyrics = None

        self.request_time = None
        self.result = ""
        
    def extract_name_from_path(self, path: str) -> str:
        file = path.rsplit("/", 1)
        return file[-1][:-4] if len(path) > 1 else path[:-4]

    def load_song(self, path: str) -> None:
        self.song_path = path
        self.song_name = self.extract_name_from_path(path)
        with open(path, "rb") as song:
            self.song = song.read()


    # def load_lyrics(self, path: str) -> None:
    #     self.lyrics_name = self.extract_name_from_path(path)
    #     with open(path, 'r') as lyrics:
    #         self.lyrics = lyrics.read()

    def find_lrc(self) -> None:
        try:
            self.request_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.result = syncedlyrics.search(self.song_name, providers=["Lrclib", "NetEase", "Megalobiz"])
        except Exception as e:
            print('"', e, "\" occured, skipping track -")

    # def save_ndarray_to_wav_to_file(self, audio: np.ndarray, rate: int, path) -> None:
    #     audio_segment = AudioSegment(audio[0].tobytes(), frame_rate=rate, sample_width=2, channels=1)

    #     audio_segment = audio_segment.normalize()  # Нормализация аудио
    #     audio_segment.export(path, format='wav')


    def make_lrc(self) -> None:
        self.request_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        audioadapter = AudioAdapter.default()
        self.audio, self.rate = audioadapter.load(self.song_path)
        self.rate = int(self.rate)

        print('\n>>> separating vocals...')
        hold_time = time()
        separator = Separator('spleeter:2stems')
        stems = separator.separate(self.audio)
        del stems['accompaniment']
        separator.save_to_file(sources=stems, audio_descriptor="temp", destination="src")
        print('done. spent ', time() - hold_time, ' seconds')


        vocals = AudioSegment.from_wav("src/temp/vocals.wav")
        print('\n>>> retrieving nonsilent timestamps...')
        hold_time = time()
        vocals_stamps = detect_nonsilent(audio_segment=vocals, silence_thresh=vocals.dBFS-16, min_silence_len=500, seek_step=2)
        print('done. spent ', time() - hold_time, ' seconds')

        model = whisper.load_model("small", in_memory=True).to("cpu")
        print('\n>>> transribing vocals...')
        hold_time = time()
        
        for stamp in vocals_stamps:
            start = stamp[0]/1000
            end = stamp[1]/1000
            
            vocals[stamp[0]:stamp[1]].export("src/temp/segment.wav", format='wav')
                        
            segment = model.transcribe("src/temp/segment.wav", language="en", temperature=0.0, word_timestamps=False)
            self.result += f'\n[{int(start//60):02}:{start%60:05.2f}] ' + segment['text'] #  - [{int(end//60):02}:{end%60:05.2f}] - |the end timestamp
        
        print('done. spent ', time() - hold_time, ' seconds')


# test function for Processing class
def test_Processing() -> None:
    p = Processing
    song_path = "tests/queen - All Dead, All Dead.mp3"
    p.load_song(path=song_path)
    p.make_lrc()
    print(p.result)


if __name__ == "__main__":
    test_Processing()