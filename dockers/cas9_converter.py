from classes.Cas9 import Cas9

def convert_cas9_to_tuple(key: int, guide: Cas9) -> (int, str, str, str, str, any, any):
    return (key,
            guide.downstream_5_prim,
            guide.downstream_3_prim,
            guide.stranded_guide_seq,
            guide.pam,
            guide.repair_profile,
            guide.repair_stats)