import random

def dice_roll(dice_set: str = '1d6',  times: int = 1):
    dice_set = dice_set.replace('D', 'd')
    params = dice_set.split('d')
    dice_qnt, dice = params[0], params[1]

    if dice_qnt == '':
        dice_qnt = dice_qnt.replace('', '1')

    dice_qnt, dice = int(dice_qnt), int(dice)

    results = []
    for _ in range(times):
        rolls = []
        for _ in range(dice_qnt):
            rolls.append(str(random.randint(1, dice)))
        summ = 0
        for s in rolls:
            summ += int(s)
        results.append(dict(rolls = rolls, summ = summ)) 

    return results
    
def roll_percent():
    return str(random.randint(1, 100))

def roll_coin():
    return random.choice(['heads', 'tail'])