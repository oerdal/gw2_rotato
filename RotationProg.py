import sys
import base64
import requests
from Weapon import Weapon, Loadout

# [&DQEQOw0aPjpLF0sXNgF6FlMXAABHAQAANwEAAAAAAAAAAAAAAAAAAAAAAAA=]
def main():
    # build = load_build()
    # # print(build)
    # if build:
    #     if build['specs']:
    #         pass
    # print(build['specs'])

    build = {'specs' : {'id': 62, 'name': 'Firebrand', 'profession': 'Guardian', 'elite': True, 'minor_traits': [2089, 2062, 2148], 'major_traits': [2075, 2101, 2086, 2063, 2076, 2116, 2105, 2179, 2159], 'weapon_trait': 2073, 'icon': 'https://render.guildwars2.com/file/6D18B2D3EE0BFA0E4BC851A7D3C39D4330250916/1769890.png', 'background': 'https://render.guildwars2.com/file/7E6454FF9A13DBE93873AF72E192A74622990171/1769899.png', 'profession_icon_big': 'https://render.guildwars2.com/file/AA12C93CBF5D25E40409060D5CD69E27F72B0892/1770210.png', 'profession_icon': 'https://render.guildwars2.com/file/A1287D0FD1159CAC3A58C212C94A4BD0AB32A8D3/1770211.png'}}
    gear = load_gear(build['specs'])
    
    
def load_gear(specs):
    profession = specs['profession']
    base_url = 'https://api.guildwars2.com/v2/professions/'
    url = base_url + profession
    r = requests.get(url)
    if r.ok:
        prof_data = r.json()
        # print(prof_data)

        gear = {}
        gear['weapons'] = load_weapons(prof_data)

        return gear
        

def load_weapons(prof_data):
    all_weapons = []
    for k, v in prof_data['weapons'].items():
        w = Weapon(k, v)
        all_weapons.append(w)
    print('weapons loaded')
    l = Loadout(all_weapons)

    return {'ws1': select_weapons(l), 'ws2': select_weapons(l)}


def select_weapons(l):
    print(l)
    while(True):
        print('Select a Mainhand or a Two Hand weapon: ')
        w1_name = input().lower()
        w1 = l.get_weapon_by_name(w1_name)
        if w1:
            if w1.is_weapon_type('Mainhand'):
                while(True):
                    print('Select an Offhand weapon: ')
                    w2_name = input().lower()
                    w2 = l.get_weapon_by_name(w2_name)
                    if w2 and w2.is_weapon_type('Offhand'):
                        return (w1, w2)
                        
            elif w1.is_weapon_type('TwoHand'):
                return w1

            else:
                print('wrong hand')
        else:
            print('not a usable weapon')


def load_build():
    print('Enter a Build Chat Link:')
    # build_link = input()
    build_link = '[&DQEQOw0aPjpLF0sXNgF6FlMXAABHAQAANwEAAAAAAAAAAAAAAAAAAAAAAAA=]'

    decoded_build = base64.b64decode(build_link)
    build_hex = decoded_build.hex()
    build_arr = [build_hex[i:i+2] for i in range(len(build_hex)) if i%2==0]

    for i in range(2, 7, 2):
        specs = get_specializations(build_arr[i])
        if specs:
            traits = get_traits(build_arr[i+1], specs)
            print(specs['name'], [t['name'] for t in traits])
    
    return {'link' : build_link,
            'specs': specs,
            'traits': traits}


def hex_to_int(byte):
    return int(byte, 16)


def get_specializations(byte):
    prof_id = hex_to_int(byte)
    # print(f'id: {prof_id} | byte: {byte}')
    base_url = 'https://api.guildwars2.com/v2/specializations/'
    url = base_url + str(prof_id)
    r = requests.get(url)
    if r.ok:
        spec_data = r.json()
        return spec_data
    return None


def get_traits(byte, spec):
    trait_bits = ('000000' + bin(int(byte, 16))[2:])[-6:]
    # print(f'id: {trait_bits} | byte: {byte}')
    trait_ids = [int(trait_bits[i:i+2], 2) for i in range(len(trait_bits)) if i%2==0]
    trait_ids.reverse()
    traits = spec['major_traits']
    traits = [traits[i:i+3] for i in range(len(traits)) if i%3==0]
    selected_traits = [traits[i][t-1] if t>0 else '' for i, t in enumerate(trait_ids)]

    trait_data = []
    for trait in selected_traits:
        base_url = 'https://api.guildwars2.com/v2/traits/'
        url = base_url + str(trait)
        r = requests.get(url)
        if r.ok:
            trait_data.append(r.json())
    return trait_data


if __name__ == '__main__':
    main()
