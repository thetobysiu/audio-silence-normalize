# SIU KING WAI SM4701 Deepstory
""" rename file with transcription to verify"""
import csv
import sys
import shutil
import os
import glob
import pandas as pd


def rename(voice):
    audio_list = glob.glob(f'{voice}_combined/*.wav')
    script = pd.read_csv(f'{voice}_all.csv',
                         encoding='utf-8', header=None, sep='|', quoting=csv.QUOTE_NONE, index_col=[0])
    for path in audio_list:
        filename = os.path.splitext(os.path.basename(path))[0]
        base_filename = filename.split("_")[0]
        if '|' not in path:
            try:
                shutil.move(path, f'{voice}_combined/{filename}|{script.loc[base_filename, 2]}|.wav')
            except:
                print('Audio not in script.')


if __name__ == '__main__':
    rename(sys.argv[1])
    print('done')
