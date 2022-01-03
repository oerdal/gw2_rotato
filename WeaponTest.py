import requests
from Weapon import Weapon

r = requests.get('https://api.guildwars2.com/v2/professions/Warrior')
if r.ok:
    data = r.json()
    all_weapons = data['weapons']

    axe = Weapon('Axe', all_weapons['Axe'])
    

    