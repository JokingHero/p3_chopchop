#!/usr/bin/env python2.7
import argparse
import sys
import codecs
import pickle

import Cas9Emulation as c9



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repairPrediction", choices=['mESC', 'U2OS', 'HEK293', 'HCT116', 'K562'], required=True,
                        help="The repair prediction type to run.")

    return parser.parse_args()

def run_repair_predictions(guides, repair_predictions):
    sys.path.append("inDelphi/")

    from inDelphi import inDelphi

    inDelphi.init_model(celltype=repair_predictions)

    for i, guide in enumerate(guides):
        try:

            left_seq = guide.downstream5prim + guide.strandedGuideSeq[:-(len(guide.PAM) + 3)]
            left_seq = left_seq[-60:]

            right_seq = guide.strandedGuideSeq[-(len(guide.PAM) + 3):] + guide.downstream3prim
            right_seq = right_seq[:60]

            seq = left_seq + right_seq
            cut_site = len(left_seq)

            # TODO remove
            # On error, inDelphi.predict returns a string, rather than a tuple, throwing a ValueError.
            pred_df, stats = inDelphi.predict(seq, cut_site)
            pred_df = pred_df.sort_values(pred_df.columns[4], ascending=False)

            guide.repProfile = pred_df
            guide.repStats = stats
        except ValueError:
            pass

    return guides

def main():
    args = parse_args()
    guides = []
    for t in c9.recv_tuples():
        guides.append(c9.tuple_to_cas9(t))

    scored_guides = run_repair_predictions(guides, args.repairPrediction)

    # If repair predictions did not run, return exit code 1
    if not scored_guides:
        exit(1)

    tuples = []
    for guide in scored_guides:
        tuples.append(c9.cas9_to_reduced_tuple(guide))

    # Encode & print the pickled tuples to STDOUT for the main script to catch.
    print codecs.encode(pickle.dumps(tuples), 'base64').decode()


if __name__ == '__main__':
    main()
