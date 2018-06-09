# 產生反轉索引, 用 python dict, list, set 模擬測試
# 做 maximum matching, 當作判斷結果

import os
import re
import json
import hashlib
import featExtractor
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pydub import AudioSegment
from collections import Counter
from operator import itemgetter
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion

if __name__ == "__main__":

    SAMPLING_RATE = 44100
    FEATLIST = '../storage/flist/featuresList'
    TEST_CLIP_DIR = '../storage/clips/'

    # load features list
    with open(FEATLIST, 'r') as fp:
        features = json.load(fp)

    invidx = {}
    # build inverted index
    for key, val in features.items():
        for fpt in val:
            try:
                invidx[fpt].append(key)
            except:
                invidx[fpt] = [key]
    # remove redundent
    for key, val in invidx.items():
        invidx[key] = list(set(invidx[key]))

    # inverted index search
    classfy = []
    items = os.listdir(TEST_CLIP_DIR)
    for item in items:
        classfy.clear()
        sound = AudioSegment.from_file(TEST_CLIP_DIR + item).set_channels(1).set_frame_rate(SAMPLING_RATE)
        samples = sound.get_array_of_samples()
        thisFeats = list(featExtractor.fingerprint(samples))
        thisFeats = list(set([x[0] for x in thisFeats]))
        # iterate fingerprints (a.k.a. the keywords)
        for keyword in thisFeats:
            try:
                classfy.extend(invidx[keyword])
            except:
                pass
        # maximum matching
        resultlist = [[key, cnt] for key, cnt in Counter(classfy).items()]
        try:
            result = max(resultlist, key = itemgetter(1)) # 0:key, 1:cnt
            print('Classified result: {0} --> {1}\tRate:{2}'.format(item, result, result[1] / len(thisFeats)))
        except:
            print('Music: {0} not found'.format(item))
