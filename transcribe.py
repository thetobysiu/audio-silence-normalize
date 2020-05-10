# SIU KING WAI SM4701 Deepstory
# Please create a folder _test
import numpy as np
import csv
import scipy.io.wavfile as wav
from deepspeech import Model
import os
import sys
import glob
import pandas as pd
ds = Model('deepspeech-0.7.0-models.pbmm')


def transcribe(path='', array=None, silence=0.3):
    if array is not None:
        audio = array
    else:
        sr, audio = wav.read(path)
        audio = np.pad(audio, (int(sr * silence), int(sr * 0.5)), 'constant')
    return ds.stt(audio)


def main(voice):
    audio_list = glob.glob(f'{voice}_test/*.wav')
    transcription = pd.DataFrame(audio_list, columns=['path'])
    transcription['filename'] = transcription['path'].str.split('.', expand=True)[0].apply(lambda x: os.path.split(x)[1])
    transcription['script'] = transcription['path'].apply(transcribe)
    transcription.drop(columns=['path'], inplace=True)
    transcription.to_csv(f'{voice}_transcription.csv', encoding='utf-8', index=False, sep='|', quoting=csv.QUOTE_NONE)
    print('done')


if __name__ == '__main__':
    main(sys.argv[1])
