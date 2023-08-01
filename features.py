import utils
import random

def get_feature_list():
    features = utils.fetch_resource("features")
    return features

def get_feature(featureId):
    feature = utils.fetch_resource(f"features/{featureId}")
    return feature

def get_random_feature():
    chosen_feature = random.choice(get_feature_list())
    feature_data = get_feature(chosen_feature["index"])
    return feature_data