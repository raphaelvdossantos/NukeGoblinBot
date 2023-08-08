import os
import random
import json

import discord

from discord.ext import commands
from dotenv import load_dotenv

import utils
import spells
import rolls

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
        'Your lullaby would waken a drunken goblin!'
    ]

    response = random.choice(quotes)
    await tlk.send(response)


@bot.command(name='fumble', help='Generates a random crit scenario')
async def fumble(fumble_response):
    with open('fumble.json') as f:
        fumble_list = json.loads(f.read())

    fumble_roll = random.randint(1, 100)
    fumble_lower = 0
    fumble_upper = 0

    for fumble in fumble_list['fumble']:
        if fumble_roll > fumble['value']:
            fumble_lower = fumble['value']
            pass
        elif fumble_roll <= fumble['value']:
            fumble_upper = fumble['value']
            message = fumble['effect']
            break

    await fumble_response.send(f"[ {fumble_lower}% - {fumble_upper}% ] : {message}")


@bot.command(name='roll', help='Rolls a dice or a set of dices N times. It can be used to make multiple rols.\n'
                               'Examples: !roll 4d6 6 (Rolls 4d6 6 times)\n'
                               '          !roll d4 2 (Rolls a d4 2 times)')
async def simple_roll(roll, dice_set: str = '1d6',  times: int = 1):
    result = rolls.dice_roll(dice_set, times)
    message = ""
    for r in result:
        message +=(f'Rolls ({ " + ".join(r["rolls"])}): {r["summ"]} \n')
    
    await roll.send(message)


@bot.command(name='percent', help='Rolls a percentage dice.')
async def roll_percent(percent):
    await percent.send(rolls.roll_percent())


@bot.command(name='luck', help='Flips a coin.')
async def roll_luck(luck):
    await luck.send('The coin flipped ' + rolls.roll_coin())


@bot.command(name='spells', help='Show a list of spells of a given level (default:1) from a given school.')
async def show_spell_list(show_spells, level: str = '1', school=''):
    spell_list = spells.get_spell_list(level, school)

    await show_spells.send(utils.format_spell_list_message(spell_list, level, school))


@bot.command(name="spell", help="Displays information of a given spell based on its id (spell name in lowercase, dash-separated. e.g.: disguise-self).")
async def get_spell(get_spell, spell_id):
    if spell_id is None:
        await get_spell.send("Spell id not informed. Please provide a spell id consisting of the spell's name in lowercase, dash-separated. e.g.: disguise-self).")
    else:
        message = utils.format_spell_message(spells.get_spell_by_id(spell_id))
    
    await get_spell.send(message)


@bot.command(name='rspell', help='Shows a random spell of a given school and level (default level = "1" & school = "illusion").')
async def choose_random_spell(random_spell, level: str = '1',school='illusion'):
    chosen_spell = spells.get_random_spell(level, school)
    await random_spell.send('The chosen spell was: ' + chosen_spell['name'])


if __name__ == "__main__":
    bot.run(TOKEN)
