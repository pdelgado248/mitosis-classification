#Automatic validation split of 0.43 of the training data

import argparse
import json
from pathlib import Path

import pandas as pd
import numpy as np
import os

from .utils import get_n_frames, get_n_frames_hdf5


def convert_csv_to_dict(csv_path, subset):
    data = pd.read_csv(csv_path)
    keys = []
    key_labels = []
    for i in range(data.shape[0]):
        row = data.iloc[i, :]
        basename = row['name']
        keys.append(basename)
        #~~~~~~~~~~~~~~~~~~~~~~~~
        #if subset != 'testing':
        
        key_labels.append(row['label'])

    database = {}
    count=0
    for i in range(len(keys)):
        key = keys[i]
        database[key] = {}
        database[key]['subset'] = subset
        #~~~~~~~~~~~~~~~~~~~~~~~~
        
        if subset != 'testing':
            label = key_labels[i]
            database[key]['annotations'] = {'label': label}
        
        else:

            label = key_labels[i]
            #print(count,' - ',key,': ',label)
            database[key]['annotations'] = {'label': label}
        #    database[key]['annotations'] = {}

    return database


def load_labels(train_csv_path):
    data = pd.read_csv(train_csv_path)
    return data['label'].unique().tolist()


def convert_mitoses_csv_to_json(train_csv_path, test_csv_path,
                                 video_dir_path, video_type, dst_json_path,split_val = 0.43):
                                     
                                     
    labels = load_labels(train_csv_path)
    train_database = convert_csv_to_dict(train_csv_path, 'training')

                                         
    #Extract validation data from the training set. No need for a validation csv file                                     
    #~~~~~~~~~~~~~~~~~~~~~~~~    
    indexes = np.arange(len( train_database))
    nbval = int(split_val * len( train_database))
    nbtrain = len( train_database) - nbval
    
    np.random.seed(699)
    val = np.random.permutation(indexes)[:nbval]
    indexes = np.array([i for i in indexes if i not in val])
 
    valDatasetNames  = np.array(list(train_database))[val]
    valDatasetValues = np.array(list(train_database.values()))[val]
    for i in range(len(valDatasetValues)):
        valDatasetValues[i]['subset'] = 'validation'
    val_database = dict(zip(valDatasetNames,valDatasetValues))
                                     
    trainDatasetNames  = np.array(list(train_database))[indexes]
    trainDatasetValues = np.array(list(train_database.values()))[indexes]
    train_database = dict(zip(trainDatasetNames,trainDatasetValues))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if os.path.exists(test_csv_path):
        test_database = convert_csv_to_dict(test_csv_path, 'testing')

    dst_data = {}
    dst_data['labels'] = labels
    dst_data['database'] = {}
    dst_data['database'].update(train_database)
    dst_data['database'].update(val_database)
    if os.path.exists(test_csv_path):
        dst_data['database'].update(test_database)

    for k, v in dst_data['database'].items():
        if 'label' in v['annotations']:
            label = v['annotations']['label']
        else:
            label = 'test'

        if video_type == 'jpg':
            video_path = video_dir_path / label / k
            if os.path.exists(video_path):
                n_frames = 12
                v['annotations']['segment'] = (1, n_frames + 1)
        else:
            video_path = video_dir_path /label / f'{k}.hdf5'
            if os.path.exists(video_path):
                n_frames = get_n_frames_hdf5(video_path)
                v['annotations']['segment'] = (0, n_frames)

    with open(dst_json_path,'w') as dst_file:
        json.dump(dst_data, dst_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path',
                        default=None,
                        type=Path,
                        help=('Directory path including '
                              'train.csv, val.csv, '
                              '(test.csv (optional))'))
    parser.add_argument(
        'n_classes',
        default=2,
        type=int,
        help='2')
    parser.add_argument('video_path',
                        default=None,
                        type=Path,
                        help=('Path of video directory (jpg or hdf5).'
                              'Using to get n_frames of each video.'))
    parser.add_argument('video_type',
                        default='jpg',
                        type=str,
                        help=('jpg or hdf5'))
    parser.add_argument('dst_path',
                        default=None,
                        type=Path,
                        help='Path of dst json file.')

    parser.add_argument('split_val',
                        default=None,
                        type=float,
                        help='Validation proportion')
    
    
    
    args = parser.parse_args()

    print(args)
    assert args.video_type in ['jpg', 'hdf5']

    train_csv_path = (args.dir_path /
                      'trainData.csv')
    test_csv_path = (args.dir_path /
                     'testData.csv')




    convert_mitoses_csv_to_json(train_csv_path, test_csv_path,args.video_path,args.video_type,args.dst_path,args.split_val)
