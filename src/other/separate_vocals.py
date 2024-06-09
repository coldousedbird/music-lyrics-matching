import openunmix
from openunmix.model import OpenUnmix
from openunmix.predict import separate
import librosa
import numpy as np
from pydub import AudioSegment
# from librosa.core import griffinlim
import torch
import torchaudio

import time


def ndarray_to_wav(audio_ndarray, rate, path):
    audio_segment = AudioSegment(audio_ndarray[0].tobytes(), frame_rate=rate, sample_width=2, channels=2)
    # Шумоподавление
    # audio_segment = audio_segment.apply_gain(-20.0)  # Применение шумоподавления
    audio_segment = audio_segment.normalize()  # Нормализация аудио
    audio_segment.export(path, format='wav')

# def spectrogram_to_mp3(spectrogram, path):
#     # Reconstruct the audio signal from the spectrogram
#     reconstructed_audio = griffinlim(spectrogram)
#     # Convert the reconstructed audio to a Pydub AudioSegment
#     reconstructed_pydub = AudioSegment(
#         reconstructed_audio.tobytes(),
#         frame_rate=audio.frame_rate,
#         sample_width=2,
#         channels=2
#     )

#     # Export the reconstructed audio
#     reconstructed_pydub.export(path, format="mp3")

def separate_vocals(song_name):
    audio, sample_rate = torchaudio.load(song_name, normalize=True)
    # Rate formatting
    model_rate = 44100
    if sample_rate != model_rate:
        transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=model_rate)
        audio = transform(audio)
    # Vocal separation
    print("retrieving vocals...")
    start_time = time.time()
    estimates = separate(audio=audio, rate=model_rate, model_str_or_path="umxhq", targets=['vocals'], niter = 1, residual=True) 
    end_time = time.time()
    print(f"retrieveing spent {end_time - start_time} seconds")

    return estimates['vocals'].numpy()[0], model_rate

    
def enhance_vocals(song_name):
    audio, sample_rate = torchaudio.load(song_name, normalize=True)
    # Rate formatting
    model_rate = 16000
    if sample_rate != model_rate:
        transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=model_rate)
        audio = transform(audio)
    # speech separation from noise
    print("enhancment vocals...")
    start_time = time.time()
    estimates = separate(audio=audio, rate=model_rate, model_str_or_path="umxse", targets=['speech'], niter = 1, residual=True, device=torch.device('cpu')) 
    end_time = time.time()
    print(f"enhancement spent {end_time - start_time} seconds")
    
    return estimates['speech'].numpy()[0], model_rate


if __name__ == "__main__":
    # song = "/run/media/coldousedbird/data/Programming/music-lyrics-matching/data/short_dataset_mp3/genesis - Small Talk.mp3"
    song = "/run/media/coldousedbird/data/Programming/music-lyrics-matching/data/short_dataset_mp3/queen - All Dead, All Dead.mp3"
    # song = "/home/coldousedbird/Programming/music-lyrics-matching/src/other/queen - All Dead, All Dead.wav"
    
    noisey_vocals, rate = separate_vocals(song)

    noisey_vocals_path = "/home/coldousedbird/Programming/music-lyrics-matching/src/temp/vocal.wav"
    ndarray_to_wav(noisey_vocals, rate=rate, path=noisey_vocals_path)

    
    denoised_vocals, rate = enhance_vocals(noisey_vocals_path)

    denoised_vocals_path = "/home/coldousedbird/Programming/music-lyrics-matching/src/temp/denoised.wav"
    ndarray_to_wav(denoised_vocals, rate=rate, path=denoised_vocals_path)
