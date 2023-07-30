import os
import random
import json

import discord

from discord.ext import commands
from dotenv import load_dotenv

import utils

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_KEY')
GUILD = os.getenv('DISCORD_GUILD')


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



@bot.command(name='spells', help='Show a list of spells of a given level (default:1) from a given school.')
async def show_spell_list(show_spells, level: str = '1', school=''):
    query = "&school=" + school if school != "" else ""
    spells = utils.fetch_resource(f'spells?level={level}{query}')

    spell_list = []
    print("Spells: ", spells['results'])

    for spell in spells['results']:
        spell_list.append(spell['name'])

    await show_spells.send(utils.format_spell_list_message(spell_list, level, school))



@bot.command(name="spell", help="Displays information of a given spell based on its id (spell name in lowercase, dash-separated. e.g.: disguise-self).")
async def get_spell(get_spell, spell_id):
    if spell_id is None:
        await get_spell.send("Spell id not informed. Please provide a spell id consisting of the spell's name in lowercase, dash-separated. e.g.: disguise-self).")
    else:
        spell = utils.fetch_resource(f"spells/{spell_id}")
        message = utils.format_spell_message(spell)
    
    await get_spell.send(message)


@bot.command(name='rspell', help='Shows a random spell of a given school and level (default level = "1" & school = "illusion").')
async def choose_random_spell(random_spell, level: str = '1',school='illusion'):
    spell = utils.fetch_resource(f"spells?level={level}&school={school}")
    chosen_spell = random.choice(spell["results"])
    await random_spell.send('The chosen spell was: ' + chosen_spell['name'])

bot.run(TOKEN)
