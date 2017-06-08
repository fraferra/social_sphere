import sys, aubio
from aubio import source, pvoc, mfcc
from numpy import vstack, zeros, diff
import numpy as np
import os
import subprocess
import xgboost as xgb
import pickle


FILE_FOLDER = "recorded_tracks/"
EMOTION_DICT = {0: "neutral", 1:"happy", 2:"sad", 3: "angry"}
FILENAME = "recorded_tracks/file.wav"


import pyaudio
import wave
 
def record_audio(s = 4):
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

import sys, aubio
import sys
from aubio import source, pvoc, mfcc
from numpy import vstack, zeros, diff
import numpy as np
from aubio import source, pvoc, filterbank



def process_wav_file(filename,
                     samplerate = 0,
                     win_s = 4096,
                     seconds_window = 3,
                     svm = True):
    from aubio import source, pitch


    hop_s = win_s // 4
    #filename = filename.replace("b'", "")[:-1]
    filename = filename.strip()
    
    


    pitches = []
    confidences = []
    #print(filename)
    n_filters = 40              # must be 40 for mfcc
    n_coeffs = 13
    s = source(filename, samplerate, hop_s)
    
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)   
    
    p = pvoc(win_s, hop_s)
    m = mfcc(win_s, n_filters, n_coeffs, samplerate)
    n_samples = 1#s.duration / s.samplerate / seconds_window
    
    pv = pvoc(win_s, hop_s)

    f = filterbank(40, win_s)
    f.set_mel_coeffs_slaney(samplerate)

    energies = zeros((40,))
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
        pitch = pitch_o(samples)[0]
        #pitch = int(round(pitch))
        fftgrain = pv(samples)
        new_energies = f(fftgrain)
        energies = vstack( [energies, new_energies] )
        confidence = pitch_o.get_confidence()
        pitches += [pitch]
        confidences += [confidence]
        frames_read += read
        if read < hop_s: break

    mfccs1 = diff(mfccs, axis = 0)
    mfccs2 = diff(mfccs, axis = 0)
    #print mfccs.shape, mfccs1.shape, mfccs2.shape
    
    


    # total number of fra
    
    
    
    pitches = np.array(pitches)
    pitches = pitches.reshape((len(pitches),1))
#     print(pitches.shape)
#     print(mfccs1.shape)
    
    
    
    
    
    all_data = np.concatenate((mfccs[1:,:], mfccs1, mfccs2, pitches, energies[1:]), 1)
    
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
    return final
    
    
    
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


def get_emotion(l = [], filename=FILENAME):
    if len(l) >= 2:
        os.system("open %s"%(l[1]))
        filename = l[1]
        record_audio()
    loaded_model = pickle.load(open("xgboost_82_acc.pickle", "rb"))
    FILENAME2 = "recorded_tracks/file2.wav"
    if filename == FILENAME:
        #os.system("rm %s"%(FILENAME2))
        record_audio()
    
        #os.system('ffmpeg -i %s -af "highpass=f=200, lowpass=f=4000" %s'%(filename, FILENAME2))
        #filename = FILENAME2

        #print("ciao")
    X = process_wav_file(filename)
    #print(X)
    xg_test = xgb.DMatrix(X, label=np.array([0]))
    #xg_test = X
    y = loaded_model.predict(xg_test)#[0]
    print("========= Confidence =========")
    print("Prob Neutral: %2f"%(y[0][0]))
    print("Prob Happy: %2f"%(y[0][1]))
    print("Prob Sad: %2f"%(y[0][2]))
    print("Prob Angry: %2f"%(y[0][3]))
    #emotion = EMOTION_DICT[y[0]]

    emotion = EMOTION_DICT[np.argmax(y)]
    
    return emotion





if __name__ == "__main__":
    PROCESSED_FILES = []
    import pickle
#s = pickle.dumps(clf)
    #Speech (1 = neutral, 2 = calm, 3 = happy, 4 = sad, 5 = angry, 6 = fearful, 7 = disgust, 8 = surprised)

    #EMOTION_DICT = {0: "neutral", 1:"happy", 2:"sad", 3: "angry"}
    #FILENAME = "recorded_tracks/file.wav"
    #loaded_model = pickle.load(open("xgboost_77_acc.pickle", "rb"))

    loaded_model = pickle.load(open("xgboost_82_acc.pickle", "rb"))

    

    while True:
        os.system("open %s"%(sys.argv[1]))

        if len(sys.argv) > 1:
            os.system("open %s"%(sys.argv[1]))

            # X = process_wav_file(sys.argv[1])
            # print(X)
            # xg_test = xgb.DMatrix(X, label=np.array([0]))
            # #xg_test = X#xgb.DMatrix(X, label=np.array([0]))

            # y = loaded_model.predict(xg_test)#[0]
            # print(y)
            # print(loaded_model.predict_proba(xg_test))
            emotion = get_emotion(filename=sys.argv[1])#EMOTION_DICT[np.argmax(y)]
            #emotion = EMOTION_DICT[y[0]]
            #print(s.duration, s.samplerate)
            print("RESULTS: ", emotion)
            break
        else:
            # record_audio()
            # X = process_wav_file(FILENAME)
            # print(X)
            # xg_test = xgb.DMatrix(X, label=np.array([0]))
            # #xg_test = X
            # y = loaded_model.predict(xg_test)#[0]
            # print(y)
            #emotion = EMOTION_DICT[y[0]]

            emotion = get_emotion()#EMOTION_DICT[np.argmax(y)]
            #emotion = EMOTION_DICT[y]
            #print(s.duration, s.samplerate)
            print("RESULTS: ", emotion)

