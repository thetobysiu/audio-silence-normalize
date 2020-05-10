# SIU KING WAI SM4701 Deepstory
# not finished, this is to transcribe each split clips
import pandas as pd
import csv
import spacy
import copy
from spacy.tokenizer import Tokenizer
nlp = spacy.load('en_core_web_sm')
nlp_no_comma = copy.deepcopy(nlp)
sentencizer = nlp.create_pipe("sentencizer")
sentencizer_no_comma = copy.deepcopy(sentencizer)
sentencizer.punct_chars.add(',')
nlp.add_pipe(sentencizer, first=True)
nlp_no_comma.add_pipe(sentencizer_no_comma, first=True)
tokenizer = Tokenizer(nlp.vocab)

transcription = pd.read_csv('transcription.csv', encoding='utf-8', sep='|', quoting=csv.QUOTE_NONE)
original = pd.read_csv('Yennefer_all.csv',
                       encoding='utf-8', sep='|', quoting=csv.QUOTE_NONE, header=None, index_col=[0])
transcription['name'], transcription['number'] = zip(*transcription['filename'].str.split('_').tolist())
transcription.sort_values(['name', 'number'], inplace=True)
transcription.reset_index(drop=True, inplace=True)

# select by pre-filtered text (some were spells, or manually deleted by me)
transcription = transcription[transcription['name'].isin(original.index)]

# separate those who remain one audio clip
transcription_done = transcription.groupby('name').filter(lambda x: len(x['number']) == 1)
transcription = transcription.groupby('name').filter(lambda x: len(x['number']) > 1)

# referencing the original script
transcription_done['script_ok'] = transcription_done['name'].apply(lambda x: original.loc[x][2])
transcription['script_ok'] = ''


def get_sentences(index_label, column_index, no_comma=False):
    if no_comma:
        df = pd.DataFrame([sent.text for sent in nlp_no_comma(original.loc[index_label][column_index]).sents],
                          columns=['script'])
    else:
        df = pd.DataFrame([sent.text for sent in nlp(original.loc[index_label][column_index]).sents],
                          columns=['script'])
    df['counts'] = df['script'].apply(lambda x: len(tokenizer(x)))
    df.sort_values(['counts'], ascending=False, inplace=True)
    return df


for name, name_df in transcription.groupby('name'):
    transcription_sentences = name_df.dropna(axis=0)
    # syllables or word_count?
    # should not count comma first
    original_sentences = get_sentences(name, 1)

    if len(transcription_sentences) > len(original_sentences):
        original_sentences = get_sentences(name, 2)
    # elif len(transcription_sentences) == len(original_sentences):
    else:
        original_sentences_unprocessed = original_sentences
        original_sentences_processed = get_sentences(name, 2)
        if len(original_sentences_processed) > len(original_sentences_unprocessed):
            original_sentences = original_sentences_processed
        elif len(original_sentences_processed) == len(original_sentences_unprocessed):
            original_sentences_unprocessed_no_comma = get_sentences(name, 1, no_comma=True)
            original_sentences_processed_no_comma = get_sentences(name, 2, no_comma=True)
            if len(original_sentences_unprocessed_no_comma) == len(original_sentences_processed_no_comma):
                if len(original_sentences_unprocessed_no_comma) == len(transcription_sentences):
                    original_sentences = original_sentences_unprocessed_no_comma

    if len(original_sentences) > len(transcription_sentences):
        while len(original_sentences) > len(transcription_sentences):
            original_sentences.sort_values(['counts'], ascending=False, inplace=True)
            last = original_sentences.iloc[-1, :]
            if last.name != 0:
                prev = original_sentences.loc[last.name - 1, :]
                lowest_counts = original_sentences[original_sentences['counts'] == last['counts']]
                if len(lowest_counts) > 1:
                    if all(lowest_counts['script'].str[-1] == ','):
                        if len(lowest_counts) > 2:
                            first = lowest_counts.iloc[0]
                            second = lowest_counts.iloc[1]
                            original_sentences.loc[second.name - 1, :] = first.apply(
                                lambda x: ' '.join([x, second['script']])
                                if isinstance(x, str) else x + second['counts'])
                            original_sentences.drop([second.name], inplace=True)
                            continue
                if last.name != max(original_sentences.index):
                    _next = original_sentences.loc[last.name + 1, :]
                    if last['script'][-1] == ',' and _next['script'][-1] != ',' and ',' not in _next['script'] and prev['script'][-1] != ',':
                        prev = last
                        last = original_sentences.loc[prev.name + 1, :]
                if prev['script'][-1] == '.' and last['script'][-1] == ',':
                    last = prev
                    prev = original_sentences.loc[last.name - 1, :]

                original_sentences.loc[last.name - 1, :] = prev.apply(
                    lambda x: ' '.join([x, last['script']]) if isinstance(x, str) else x + last['counts'])
                original_sentences.drop([last.name], inplace=True)
            else:
                original_nlp = nlp(last['script'])
                transcription_nlp = nlp(transcription_sentences.iloc[0]['script'])

    original_sentences.sort_index(inplace=True)
    for i, (trans_index, row) in enumerate(transcription_sentences.iterrows()):
        row['script_ok'] = original_sentences.iloc[i]['script']
        transcription.loc[trans_index, :] = row
    print('hi')
print('done')
