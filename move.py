# SIU KING WAI SM4701 Deepstory
import csv
import sys
import shutil
import pandas as pd
sr = 22050

# move audios with transcription back to output folder, leave the unidentified to be renamed


def move(voice):
    audio_transcript = pd.read_csv(
        f'{voice}_transcription.csv', encoding='utf-8', sep='|', quoting=csv.QUOTE_NONE, index_col=['filename'])
    audio_transcript.dropna(inplace=True)
    for filename in audio_transcript.index:
        try:
            shutil.move(f'{voice}_test/{filename}.wav', f'{voice}_output/{filename}.wav')
        except:
            print(f'{filename} is not found!')


if __name__ == '__main__':
    move(sys.argv[1])
    print('done')
