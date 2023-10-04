import billiard as mp
import sys
import os
from scipy.io.wavfile import write as write_wav
import librosa
from tqdm.auto import tqdm
import pandas as pd
import numpy as np
import miditoolkit

from utils.config import *
from synthesizer.NoteSynthesizer import NoteSynthesizer

Nsynth_dir = sys.argv[1]
data_folder = sys.argv[2]
output_dir = sys.argv[3]

csv_path = os.path.join(data_folder, 'balanced', 'balanced_mata.csv')
midi_df = pd.read_csv(csv_path)

train_idx = midi_df[midi_df['split_data'] == 'train'].index.values
val_idx = midi_df[midi_df['split_data'] == 'val'].index.values
test_idx = midi_df[midi_df['split_data'] == 'test'].index.values

file_list = list()

for idx, v in enumerate(midi_df['id']):
    split = midi_df['split_data'].values[idx]
    if split == 'train':
        current_file = split + '/augmented/' + v + '.mid'
        file_list.append(os.path.join(data_folder, current_file))
    elif split == 'val':
        current_file = split + '/raw/' + v + '.mid'
        file_list.append(os.path.join(data_folder, current_file))
    elif split == 'test':
        current_file = split + '/raw/' + v + '.mid'
        file_list.append(os.path.join(data_folder, current_file))

train_file_list = [file_list[i] for i in train_idx]
val_file_list = [file_list[i] for i in val_idx]
test_file_list = [file_list[i] for i in test_idx]
selected_file_list = train_file_list + val_file_list + test_file_list

def inst_to_map(inst):
    number = INST_MAP[inst]
    return INST_FAM_dict[number]

def get_instrument_family(df):
    df['instrument_str'] = df['inst'].apply(lambda x: x.split('-')[0])
    df['instrument_str'] = df['instrument_str'].apply(lambda x: inst_to_map(x))
    return df

midi_df = get_instrument_family(midi_df)

for idx, v in enumerate(midi_df['track_role']):
    if v == 'bass':
        midi_df.loc[idx, 'instrument_str'] = 'bass'

print('Number of files: ', len(selected_file_list))
print('preparing to synthesize...')

synth = NoteSynthesizer(dataset_path=-Nsynth_dir, csv_path=csv_path, output_dir=output_dir, sr=NSYNTH_SAMPLE_RATE)

cnt_cpu = mp.cpu_count() - 2
pool = mp.Pool(cnt_cpu)

print('CPU count: ', cnt_cpu)
print('start synthesizing...')

output_dict = {'id': [], 'instrument': [], 'preset': [], 'source': []}
total = len(selected_file_list)

with tqdm(total=total) as pbar:
    for dict_object in tqdm(pool.imap_unordered(synth.render_sequence, selected_file_list)):
        for k, v in dict_object.items():
            output_dict[k].append(v)
        pbar.update()

pool.close()

print('saving csv...')

output_df = pd.DataFrame(output_dict)
output_df.to_csv(os.path.join(output_dir, 'synthesized_results.csv'), index=False)