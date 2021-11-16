#!/usr/bin/env python3
import argparse
import sys
import codecs
import pickle
import pandas as pd

from dockers import Cas9Emulation as c9

import numpy as np
from tensorflow.keras.models import load_model

def run_croton_predictions(guides):

    model = load_model('models/CROTON.h5')  # load multitask model

    for i, guide in enumerate(guides):
        try:

            left_seq = guide.downstream5prim + guide.strandedGuideSeq[:-(len(guide.PAM) + 3)]
            left_seq = left_seq[-60:]

            right_seq = guide.strandedGuideSeq[-(len(guide.PAM) + 3):] + guide.downstream3prim
            right_seq = right_seq[:60]

            seq = left_seq + right_seq
            mid_seq = seq[30:90].decode("utf-8")

            seq = one_hot_encode(mid_seq, 'ACGT')
            seq = np.reshape(seq, (1, 60, 4))
            cut_site = len(left_seq)

            pred_arr = model.predict(seq)
            pred = pd.DataFrame(pred_arr, columns = ["del_freq","1_bp_ins","1_bp_del","1_bp_fram","2_bp_fram","fram_freq"])
            pred_stats = build_stats(pred)

            guide.repProfile = pred
            guide.repStats = pred_stats
        except ValueError:
            pass

    return guides

def one_hot_encode(seq, base_map):
    seq = seq.upper()
    mapping = dict(zip(base_map, range(4)))
    seq2 = [mapping[i] for i in seq]
    return np.eye(4)[seq2]


def build_stats(pred):

    del_freq = pred.loc[0,'del_freq']
    one_bp_ins = pred.loc[0,'1_bp_ins']
    one_bp_del = pred.loc[0,'1_bp_del']
    one_bp_fram = pred.loc[0,'1_bp_fram']
    two_bp_fram = pred.loc[0,'2_bp_fram']
    fram_freq = pred.loc[0, 'fram_freq']


    stats = {'Deletion frequency': del_freq.item()*100,
             '1 bp insertion probability': one_bp_ins.item()*100,
             '1 bp deletion probability': one_bp_del.item()*100,
             '1 bp frameshift frequency': one_bp_fram.item()*100,
             '2 bp frameshift frequency': two_bp_fram.item()*100,
             'Frameshift frequency': fram_freq.item()*100,
             }
    return stats

def main():

    guides = []
    for t in c9.recv_tuples():
        guides.append(c9.tuple_to_cas9(t))

    scored_guides = run_croton_predictions(guides)

    if not scored_guides:
        exit(1)

    tuples = []
    for guide in scored_guides:
        tuples.append(c9.cas9_to_reduced_tuple(guide))

    # Encode & print the pickled tuples to STDOUT for the main script to catch.
    print(codecs.encode(pickle.dumps(tuples), 'base64').decode())

if __name__ == "__main__":
    main()