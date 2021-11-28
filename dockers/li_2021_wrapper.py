import codecs
import pickle
import subprocess

from classes.Cas9 import Cas9
from dockers.cas9_converter import convert_cas9_to_tuple

def run_croton_prediction(guides: [Cas9]) -> [Cas9]:
    """
    Runs chopchop_li_2021 docker image using the supplied guides & repair prediction mode.

    :param repair_prediction: The repair mode to use.
    :param guides: A list of Cas9 objects to score.
    :return: Returns a list of Cas9 scored objects.
    """

    keyed_tuples = []
    for key, guide in enumerate(guides):
        keyed_tuples.append(convert_cas9_to_tuple(key, guide))

    encoded = codecs.encode(pickle.dumps(keyed_tuples, protocol=2), 'base64').decode()

    decoded = pickle.loads(codecs.decode(encoded.encode(), 'base64'))

    command = ['docker', 'run', '-i', 'chopchop_li_2021']

    repair_prediction = subprocess.run(command, capture_output=True, text=True, input=encoded)

    # encoding='latin1' is for backwards compatibility.
    results = pickle.loads(codecs.decode(repair_prediction.stdout.encode(), 'base64'), encoding='latin1')

    for key, guide in enumerate(guides):
        for t in results:
            if t[0] == key:
                _, guide.repair_profile, guide.repair_stats = t

    return guides