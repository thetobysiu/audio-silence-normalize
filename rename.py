import csv
import sys
import shutil
import os
import glob
import pandas as pd


def rename(voice):
    audio_list = glob.glob(f'{voice}_test/*.wav')
    script = pd.read_csv(f'{voice}_all.csv',
                         encoding='utf-8', header=None, sep='|', quoting=csv.QUOTE_NONE, index_col=[0])
    for path in audio_list:
        filename = os.path.splitext(os.path.basename(path))[0]
        base_filename = filename.split("_")[0]
        if '|' not in path:
            try:
                shutil.move(path, f'{voice}_test/{filename}|{script.loc[base_filename, 2]}|.wav')
            except:
                print('Audio not in script.')
        if not os.path.isfile(f'{voice}_test/{base_filename}.wav'):
            shutil.copy(f'{voice}/{base_filename}.wav', f'{voice}_test/{base_filename}.wav')


if __name__ == '__main__':
    rename(sys.argv[1])
    print('done')
