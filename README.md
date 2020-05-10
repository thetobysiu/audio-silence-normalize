## Intro
Normalize the silence duration of audio to make comma/silence trainable in DCTTS.

Since sometimes an audio clip contains multiple sentences, and each sentences sometimes have longer or shorter pause, it's necessary to pre-process audio data in order for it to be used in DCTTS.

It first split audio so that all silence goes away, and then insert back a fixed duration of silence between the split audio clips.

## Steps
Usage X.py Geralt
1. Place the respective character audio folder in the root and run split.py, the Geralt_output folder will be created containing the split clips.
2. (optional) select audio clips that are really small(likely to be sign and hmm) and move into a folder named _test, e.g. Geralt_test
3. (optional) run transcribe.py, it will transcribe all the clips, {voice}_transcription.csv will be created
4. (optional) run move.py, it reads the transcription.csv and move all the files with transcription from test folder back to output folder
5. (optional) run rename.py, it rename the remaining clips in test folder with the sentence as the filename for easier manual checking
6. (optional) after checking and deleting, the remaining clips in test folder should be retained, run clean.py to rename it back to normal and move back to output folder
7. run combine.py to merge the clips and insert fixed silence between clips. A folder {voice}_combined will be created.

## Tools
convert_16k.sh to convert all audios to 16k (required for deepspeech transcribe)
convert_22k.sh to convert all audios to 22k