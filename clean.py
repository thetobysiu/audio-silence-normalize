# SIU KING WAI SM4701 Deepstory
import sys
import shutil
import os
import glob
import re


def clean(voice):
    audio_list = glob.glob(f'{voice}_test/*.wav')
    for path in audio_list:
        filename = os.path.splitext(os.path.basename(path))[0]
        if '_' in filename:
            if '|' in path:
                filename = re.sub(r'\|.*\|', '', filename)
            shutil.move(path, f'{voice}_output/{filename}.wav')
        else:
            os.remove(path)


if __name__ == '__main__':
    clean(sys.argv[1])
    print('done')
