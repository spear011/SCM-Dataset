import os
import sys
import random
from tqdm import tqdm
import pandas as pd
import numpy as np

commu_folder = sys.argv[1]
commu_meta = pd.read_csv(os.path.join(commu_folder, 'commu_meta.csv'), index_col=0)

def index_select(idx, num):
    random.shuffle(idx)
    return idx[:num]

def get_idx_list(commu_meta):
    labels = commu_meta['track_role'].values.tolist()
    
    m_melody_idx =[i for i, v in enumerate(labels) if v == 'main_melody']
    s_melody_idx = [i for i, v in enumerate(labels) if v == 'sub_melody']
    bass_idx = [i for i, v in enumerate(labels) if v == 'bass']
    accom_idx = [i for i, v in enumerate(labels) if v == 'accompaniment']
    riff_idx = [i for i, v in enumerate(labels) if v == 'riff']
    pad_idx = [i for i, v in enumerate(labels) if v == 'pad']

    m_melody_idx = index_select(m_melody_idx, 500)
    s_melody_idx = index_select(s_melody_idx, 500)
    bass_idx = index_select(bass_idx, 500)
    accom_idx = index_select(accom_idx, 500)
    riff_idx = index_select(riff_idx, 500)
    pad_idx = index_select(pad_idx, 500)

    idx_list = [m_melody_idx, s_melody_idx, bass_idx, accom_idx, riff_idx, pad_idx]
    return idx_list

def index_split(idx, valid_ratio, test_ratio):
    random.shuffle(idx)
    test_num = int(len(idx) * test_ratio)
    test_idx = idx[:test_num]
    train_idx = idx[test_num:]
    
    valid_num = int(len(train_idx) * valid_ratio)
    valid_idx = train_idx[:valid_num]
    train_idx = train_idx[valid_num:]
    return train_idx, valid_idx, test_idx

train_idx = np.array([], dtype=int)
valid_idx = np.array([], dtype=int)
test_idx = np.array([], dtype=int)

idx_list = get_idx_list(commu_meta)

for lists in idx_list:
    train, valid, test = index_split(lists, 0.1, 0.2)
    train_idx = np.append(train_idx, train)
    valid_idx = np.append(valid_idx, valid)
    test_idx = np.append(test_idx, test)

random.shuffle(train_idx)
random.shuffle(valid_idx)
random.shuffle(test_idx)

all_idx = np.concatenate((train_idx, valid_idx, test_idx), axis=0)

balanced_df = commu_meta.loc[all_idx]
balanced_df['split'] = None

balanced_df.loc[train_idx, 'split'] = 'train'
balanced_df.loc[valid_idx, 'split'] = 'valid'
balanced_df.loc[test_idx, 'split'] = 'test'

balanced_df.reset_index(drop=True, inplace=True)

print('train samples: ', len(train_idx), 'valid samples: ', len(valid_idx), 'test samples: ', len(test_idx))

commu_midi_dir = os.path.join(commu_folder, 'commu_midi')
balanced_dir = os.path.join(commu_folder, 'balanced')

os.mkdir(balanced_dir)
os.mkdir(os.path.join(balanced_dir, 'train'))
os.mkdir(os.path.join(balanced_dir, 'valid'))
os.mkdir(os.path.join(balanced_dir, 'test'))
os.mkdir(os.path.join(balanced_dir, 'train', 'raw'))
os.mkdir(os.path.join(balanced_dir, 'valid', 'raw'))
os.mkdir(os.path.join(balanced_dir, 'test', 'raw'))

print('copying selected midi files...')

for idx, v in tqdm(enumerate(balanced_df['id'])):

    split_data = balanced_df['split_data'].values[idx]
    current_folder = os.path.join(commu_midi_dir, split_data + '/raw/')
    current_file = os.path.join(current_folder, v + '.mid')

    split = balanced_df['split'].values[idx]

    if split == 'train':
        os.system('cp ' + current_file + ' ' + os.path.join(balanced_dir, 'train', 'raw' , v + '.mid'))
    
    elif split == 'valid':
        os.system('cp ' + current_file + ' ' + os.path.join(balanced_dir, 'valid', 'raw' , v + '.mid'))
    
    elif split == 'test':
        os.system('cp ' + current_file + ' ' + os.path.join(balanced_dir, 'test', 'raw' , v + '.mid'))

balanced_df.drop(['split_data'], axis=1, inplace=True)
balanced_df.rename(columns={'split': 'split_data'}, inplace=True)

balanced_df.to_csv(os.path.join(balanced_dir, 'balanced_meta.csv'), index=False)
print('done')