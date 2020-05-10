# SIU KING WAI SM4701 Deepstory
import numpy as np
import csv
from split import trim_custom
import shutil
from more_itertools import intersperse
import scipy.io.wavfile as wav
import os
import sys
import glob
import pandas as pd
sr = 22050


def combine(voice):
    if not os.path.exists(f'{voice}_combined'):
        os.mkdir(f'{voice}_combined')
    audio_list = glob.glob(f'{voice}_output/*.wav')
    audio_df = pd.DataFrame(audio_list, columns=['path'])
    audio_df['filename'] = audio_df['path'].str.split('.', expand=True)[0].apply(lambda x: os.path.split(x)[1])
    audio_df['name'], audio_df['number'] = zip(*audio_df['filename'].str.split('_').tolist())
    audio_df.to_csv(f'{voice}_audio_df.csv', encoding='utf-8', index=False, sep='|', quoting=csv.QUOTE_NONE)

    for name, name_df in audio_df.groupby('name'):
        path_list = name_df.sort_values('number')['path'].to_list()
        if len(path_list) > 1:
            audio_slice = intersperse(np.zeros(int(sr * 1500 / 10000), dtype=np.int16), [wav.read(path)[1] for path in path_list])
            # name_audio = trim_custom(np.concatenate([*audio_slice], axis=None))
            name_audio = np.concatenate([*audio_slice], axis=None)
            wav.write(f'{voice}_combined/{name}.wav', sr, name_audio.astype(np.int16))
        else:
            shutil.copy2(path_list[0], f'{voice}_combined/{name}.wav')


if __name__ == '__main__':
    combine(sys.argv[1])
    print('done')
