#!/usr/bin/env python3
import argparse
import codecs
import pickle
import json

import Cas9Emulation as c9

from indel_prediction.predictor import predict

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-isTest", required=False,
                        help="Indicates testrun.")

    return parser.parse_args()

def run_forecast_predictions(guides, isTest):

    for i, guide in enumerate(guides):
        try:

            left_seq = guide.downstream5prim + guide.strandedGuideSeq[:-(len(guide.PAM) + 3)]
            left_seq = left_seq[-60:]

            right_seq = guide.strandedGuideSeq[-(len(guide.PAM) + 3):] + guide.downstream3prim
            right_seq = right_seq[:60]

            seq = left_seq + right_seq

            cut_site = len(left_seq)

            pred_dict, pred_stats = predict.main(seq, cut_site)
            del pred_dict['-']

            guide.repProfile = json.dumps(pred_dict)
            guide.repStats = {"Frameshift frequency":100-pred_stats}
            if isTest == "True":
                break

        except ValueError:
            pass

    return guides

def main():
    args = parse_args()

    guides = []
    for t in c9.recv_tuples():
        guides.append(c9.tuple_to_cas9(t))

    scored_guides = run_forecast_predictions(guides, args.isTest)

    if not scored_guides:
        exit(1)

    tuples = []
    for guide in scored_guides:
        tuples.append(c9.cas9_to_reduced_tuple(guide))

    # Encode & print the pickled tuples to STDOUT for the main script to catch.
    print(codecs.encode(pickle.dumps(tuples), 'base64').decode())

if __name__ == "__main__":
    main()