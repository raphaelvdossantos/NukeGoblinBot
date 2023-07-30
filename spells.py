import utils
import random

def get_spell_list(level: str = '1', school=''):
    query = "&school=" + school if school != "" else ""
    spells = utils.fetch_resource(f'spells?level={level}{query}')

    spell_list = []
    for spell in spells['results']:
        spell_list.append(spell['name'])
    
    return spell_list

def get_random_spell(level: str = '1',school='illusion'):
    spell = utils.fetch_resource(f"spells?level={level}&school={school}")
    chosen_spell = random.choice(spell["results"])

    return chosen_spell

def get_spell_by_id(spell_id):
    spell = utils.fetch_resource(f"spells/{spell_id}")
    return spell