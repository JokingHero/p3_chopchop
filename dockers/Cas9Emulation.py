
import sys
import pickle
import codecs

def recv_tuples():
    """
    Receives a Base64 encoded pickled list of tuples containing arguments for Cas9Emulation objects.

    Source: https://stackoverflow.com/q/30469575

    :return a list of tuples
    """
    pickled = sys.stdin.read()

    tuples = pickle.loads(codecs.decode(pickled.encode(), 'base64'))

    return tuples

def tuple_to_cas9(t):
    """
    Takes a tuple containing all fields of the Cas9Emulation object and returns a Cas9Emulation object.

    :param t: The tuple representation of a Cas9Emulation object.
    :return: The corresponding Cas9Emulation object.
    """

    return Cas9Emulation(*t)#Cas9Emulation.Cas9Emulation(*t)


def cas9_to_reduced_tuple(guide):
    """
    Returns a reduced tuple containing only the key & modified values of the Cas9Emulation objects after running
    repair prediction.

    :param guide: The guide to reduce into a tuple.
    :return: A tuple containing the inout guide's key, score
    """
    return guide.key, guide.repProfile, guide.repStats

class Cas9Emulation(object):
    """
    `Cas9` emulation.

    This class emulates the `Cas9` class from the main CHOPCHOP script, guides are transmitted through the argument
    parser using the `Cas9EmulationAction` class.
    """

    def __init__(self, key, downstream_5_prim, downstream_3_prim, stranded_guide_seq, pam, rep_profile, rep_stats):
        self.CoefficientsScore = {}

        # Unique identifier for each Cas9 object
        self.key = key

        # Cas9 fields used by repair predictions
        self.downstream5prim = downstream_5_prim.encode('ascii', 'ignore')
        self.downstream3prim = downstream_3_prim.encode('ascii', 'ignore')
        self.strandedGuideSeq = stranded_guide_seq.encode('ascii', 'ignore')
        self.PAM = pam.encode('ascii', 'ignore')
        self.repProfile = rep_profile
        self.repStats = rep_stats