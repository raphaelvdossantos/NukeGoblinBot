import os
import random
import json

import requests

import discord

from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_KEY')
GUILD = os.getenv('DISCORD_GUILD')

api_endpoint = "https://www.dnd5eapi.co/api/"

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='talk', help='Starts a random conversation with the bot')
async def talk(tlk):
    quotes = [
        'What is better - to be born good, or to overcome your evil nature through great effort?',
        'Be or not to Be?',
        'I rather live a simple life where I can be useful',
        'My hands has greater purpose than destroying',
    ]

    response = random.choice(quotes)
    await tlk.send(response)


@bot.command(name='roll', help='Rolls a dice or a set of dices N times. It can be used to make multiple rols.\n'
                               'Examples: !roll 4d6 6 (Rolls 4d6 6 times)\n'
                               '          !roll d4 2 (Rolls a d4 2 times)')
async def simple_roll(roll, dice_set: str = '1d6',  times: int = 1):
    dice_set = dice_set.replace('D', 'd')
    params = dice_set.split('d')
    dice_qnt, dice = params[0], params[1]
    if dice_qnt == '':
        dice_qnt = dice_qnt.replace('', '1')
    dice_qnt, dice = int(dice_qnt), int(dice)
    for _ in range(times):
        rolls = []
        for r in range(dice_qnt):
            rolls.append(random.randint(1, dice))
        response = [str(r) for r in rolls]
        summ = 0
        for s in response:
            summ += int(s)
        print('Rolls (' + ' + '.join(response) + f'): {summ}')

        await roll.send('Rolls (' + ' + '.join(response) + f'): {summ}')


@bot.command(name='fumble', help='Generates a random crit scenario')
async def fumble(fumble_response):
    with open('fumble.json') as f:
        fumble_list = json.loads(f.read())

    fumble_roll = random.randint(1, 100)

    for fumble in fumble_list['fumble']:
        if fumble_roll > fumble['value']:
            pass
        elif fumble_roll <= fumble['value']:
            message = fumble['effect']
            break

    await fumble_response.send(message)


@bot.command(name='percent', help='Rolls a percentage dice.')
async def roll_percent(percent):
    await percent.send(str(random.randint(1, 100)))


@bot.command(name='luck', help='Flips a coin.')
async def roll_luck(luck):
    await luck.send('The coin flipped ' + random.choice(['heads', 'tail']))

def format_spell_list_message(spells = [], level = "1", school = ""):
    spells_count = len(spells)
    ordered_level = f"{level}{'st' if int(level) == 1 else 'nd' if int(level) == 2 else 'rd' if int(level )== 3 else 'th'}"
    school = f"from the {school} school " if school != "" else ""
    level = f"of {ordered_level} level"
    message = f"There's a total of {spells_count} {'spells' if spells_count > 1 else 'spell'} {school}{level}:\n" + str('\n'.join(spells))

    return message

@bot.command(name='spells', help='Show a list of spells of a given level (default:1) from a given school.')
async def show_spell_list(show_spells, level: str = '1', school=''):
    query = "&school=" + school if school != "" else ""
    response = requests.get(api_endpoint + f'spells?level={level}{query}')
    spells = response.json()

    spell_list = []
    print("Spells: ", spells['results'])

    for spell in spells['results']:
        spell_list.append(spell['name'])

    await show_spells.send(format_spell_list_message(spell_list, level, school))

@bot.command(name="spell", help="Displays information of a given spell based on its id (spell name in lowercase, dash-separated. e.g.: disguise-self).")
async def get_spell(get_spell, spell_id):
    if spell_id is None:
        await get_spell.send("Spell id not informed. Please provide a spell id consisting of the spell's name in lowercase, dash-separated. e.g.: disguise-self).")
    else:
        response = requests.get(api_endpoint + spell_id)
        spell = response.json()

        message = f"Name: {spell['name']} \n"
        + f"Level: {spell['level']}     Classes: {[str(c['name'] + (',' if c['name'] != spell['classes'].at(-1)['name'] else '')) for c in spell['classes']]}"
        + f"Range: {spell['range']}     Casting Time: {spell['casting_time']}       Duration: {spell['duration']}\n"
        + f"Description: {spell['description']} \n"
    
    await get_spell.send(message)


@bot.command(name='rspell', help='Shows a random spell of a given class and level (both required).')
async def choose_random_spell(random_spell, caster='all', level: str = '1'):
    with open('./spells.json') as spell_list:
        spells = json.loads(spell_list.read())

    momentary_list = []

    for s in spells['spells']:
        if (caster in s['level']) and (s['level'][caster] == int(level)):
            momentary_list.append(s['name'])
        else:
            pass

    await random_spell.send('The chosen spell was: ' + random.choice(momentary_list))

bot.run(TOKEN)
