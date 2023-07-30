import requests

api_endpoint = "https://www.dnd5eapi.co/api/"

def fetch_resource(endpoint):
    response = requests.get(f"{api_endpoint}{endpoint}")
    data = response.json()
    return data

def format_spell_message(spell): 
    message = f"Name: {spell['name']} \n"
    + f"Level: {spell['level']}     Classes: {[str(c['name'] + (',' if c['name'] != spell['classes'].at(-1)['name'] else '')) for c in spell['classes']]}"
    + f"Range: {spell['range']}     Casting Time: {spell['casting_time']}       Duration: {spell['duration']}\n"
    + f"Description: {spell['description']} \n"
    return message

def format_spell_list_message(spells = [], level = "1", school = ""):
    spells_count = len(spells)
    ordered_level = f"{level}{'st' if int(level) == 1 else 'nd' if int(level) == 2 else 'rd' if int(level )== 3 else 'th'}"
    school = f"from the {school} school " if school != "" else ""
    level = f"of {ordered_level} level"
    message = f"There's a total of {spells_count} {'spells' if spells_count > 1 else 'spell'} {school}{level}:\n" + str('\n'.join(spells))

    return message