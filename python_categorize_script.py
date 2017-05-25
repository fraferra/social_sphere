import sys, aubio
from aubio import source, pvoc, mfcc
from numpy import vstack, zeros, diff
import numpy as np
import os
import subprocess
import xgboost as xgb

FILE_FOLDER = "recorded_tracks/"

import pyaudio
import wave
 
def record_audio(s = 3):
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = s
    WAVE_OUTPUT_FILENAME = "recorded_tracks/file.wav"

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")


    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def process_wav_file(filename,
                     samplerate = 0,
                     win_s = 4096,
                     seconds_window = 3,
                     svm = True):
    hop_s = win_s // 4
    #print(filename)
    n_filters = 40              # must be 40 for mfcc
    n_coeffs = 13
    s = source(filename, samplerate, hop_s)
    p = pvoc(win_s, hop_s)
    m = mfcc(win_s, n_filters, n_coeffs, samplerate)
    n_samples = 1#s.duration / s.samplerate / seconds_window
    if n_samples == 0:
        return []
    mfccs = zeros([n_coeffs,])
    frames_read = 0
    while True:
        samples, read = s()
        #print(samples, read)
        spec = p(samples)
        mfcc_out = m(spec)
        mfccs = vstack((mfccs, mfcc_out))
        frames_read += read
        if read < hop_s: break

    mfccs1 = diff(mfccs, axis = 0)
    mfccs2 = diff(mfccs, axis = 0)
    #print mfccs.shape, mfccs1.shape, mfccs2.shape
    all_data = np.concatenate((mfccs[1:,:], mfccs1, mfccs1), 1)
    
    final = []
    size_row = len(all_data) / n_samples
    if svm:
        final.append(get_mean_avg_etc(all_data))
    else:    
        final.append(all_data)
#     for i in range(n_samples):
#         if svm:
#             final.append(get_mean_avg_etc(all_data[i*size_row: (i+1)*size_row]))
#         else:    
#             final.append(all_data[i*size_row: (i+1)*size_row])
    return np.array(final)
    
def get_mean_avg_etc(row):
    new_row = []
    new_row += list(row.mean(axis = 0))
    new_row += list(row.std(axis = 0))
    new_row += list(row.min(axis = 0))
    new_row += list(row.max(axis = 0))
    return new_row


def get_wav_file_paths(folder_path):
    return list(map(lambda a: folder_path + str(a), 
               filter(lambda a: ".wav" in str(a), subprocess.check_output(['ls', folder_path]).splitlines())))

if __name__ == "__main__":
    PROCESSED_FILES = []
    import pickle
#s = pickle.dumps(clf)
    #Speech (1 = neutral, 2 = calm, 3 = happy, 4 = sad, 5 = angry, 6 = fearful, 7 = disgust, 8 = surprised)

    EMOTION_DICT = {0: "NEUTRAL", 1:"HAPPY", 2:"SAD", 3: "ANGRY"}
    FILENAME = "recorded_tracks/file.wav"
    loaded_model = pickle.load(open("xgboost_75_acc.pickle", "rb"))

    while True:
        record_audio()
        X = process_wav_file(FILENAME)
        xg_test = xgb.DMatrix(X, label=np.array([0]))
        y = loaded_model.predict(xg_test)
        emotion = EMOTION_DICT[np.argmax(y)]
        print("RESULTS: ", emotion)

