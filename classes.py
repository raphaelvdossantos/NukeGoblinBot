import utils
import random

def get_class_list():
    classes = utils.fetch_resource("classes")
    return classes

def get_class(classId):
    selected_class = utils.fetch_resource(f"classes/{classId}")
    return selected_class

def get_random_class():
    chosen_class = random.choice(get_class_list())
    class_data = get_class(chosen_class["index"])
    return class_data

def get_class_resource(classId, resource):
    class_resource = utils.fetch_resource(f"classes/{classId}/{resource}")
    return class_resource

def get_class_resource_by_level(classId, level, resource):
    class_resource = utils.fetch_resource(f"classes/{classId}/levels/{level}/{resource}/")
    return class_resource

def get_class_status_by_level(classId, level ):
    class_resource = utils.fetch_resource(f"classes/{classId}/levels/{level}")
    return class_resource