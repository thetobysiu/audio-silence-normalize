# SIU KING WAI SM4701 Deepstory
import librosa
import numpy as np
import librosa.display
import os
import glob
import scipy.io.wavfile as wav
import sys
sr = 22050


def split_audio_to_list(source, preemph=True, preemphasis=0.8, min_diff=1500, min_size=3000, chunk_size=9000, db=50):
    if preemph:
        source = np.append(source[0], source[1:] - preemphasis * source[:-1])
    split_list = librosa.effects.split(source, top_db=db).tolist()
    i = len(split_list) - 1
    while i > 0:
        if split_list[i][-1] - split_list[i][0] > min_size:
            now = split_list[i][0]
            prev = split_list[i - 1][1]
            diff = now - prev
            if diff < min_diff:
                split_list[i - 1] = [split_list[i - 1][0], split_list.pop(i)[1]]
        else:
            split_list.pop(i)
        i -= 1
    return [x for x in split_list if x[-1] - x[0] > chunk_size]


def trim_custom(audio, begin_db=25, end_db=40):
    begin = librosa.effects.trim(audio, top_db=begin_db)[1][0]
    end = librosa.effects.trim(audio, top_db=end_db)[1][1]
    return audio[begin:end]


def split(audio_folder):
    audio_list = glob.glob(f'{audio_folder}/*.wav')
    if not os.path.exists(f'{audio_folder}_output'):
        os.mkdir(f'{audio_folder}_output')
    # if not os.path.exists('output_16k'):
    #     os.mkdir('output_16k')

    for audio_file in audio_list:
        filename = os.path.splitext(os.path.basename(audio_file))[0]
        audio_array = librosa.load(audio_file, sr=sr)[0]
        audio_split = split_audio_to_list(audio_array)
        for i, part in enumerate(audio_split):
            part_array = trim_custom(audio_array[slice(*part)])
            # part_array_16k = librosa.resample(part_array, sr, 16000)
            part_array *= 32767
            # part_array_16k *= 32767
            wav.write(f'{audio_folder}_output/{filename}_{i}.wav', sr, part_array.astype(np.int16))
            # wav.write(f'{audio_folder}_output_16k/{filename}_{i}.wav', 16000, part_array_16k.astype(np.int16))


if __name__ == '__main__':
    split(sys.argv[1])
    print('done')
