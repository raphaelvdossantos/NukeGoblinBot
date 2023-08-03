import utils
import random

def get_feat_list():
    feats = utils.fetch_resource("feats")
    return feats

def get_feat(featId):
    feat = utils.fetch_resource(f"feats/{featId}")
    return feat

def get_random_feat():
    chosen_feat = random.choice(get_feat_list())
    feat_data = get_feat(chosen_feat["index"])
    return feat_data