import requests


class Weapon:
    # KEY_NAMES = ['specialization', 'flags', 'skills']

    def __init__(self, name, data):
        self.name = name.lower()
        self.display = name
        if 'specialization' in data:
            self.specialization = data['specialization']
        else:
            self.specialization = None
        self.flags = data['flags']
        self.skills = [skill['id'] for skill in data['skills']]
        self.skill_data = self.get_skills()
    

    def parse_flags(self):
        for flag in self.flags:
            print(flag)
    

    def get_skills(self):
        base_url = 'https://api.guildwars2.com/v2/skills?ids='
        skill_ids = self.skills
        url = base_url + ','.join([str(s) for s in skill_ids])
        print(f'request to {url}')
        r = requests.get(url)
        if r.ok:
            skill_data = r.json()
            return skill_data
        return None

    
    def is_weapon_type(self, weapon_types):
        if isinstance(weapon_types, list):
            return any([t in self.flags for t in weapon_types])
        return weapon_types in self.flags


    def __str__(self):
        return self.name


    def __repr__(self):
        return self.display


class Loadout:

    def __init__(self, weapons):
        self.weapons = weapons
        self.weapon_dict = {w.name: w for w in weapons}
    

    def get_mainhand_weapons(self):
        return self.filter_by_type('Mainhand')


    def get_offhand_weapons(self):
        return self.filter_by_type('Offhand')


    def get_twohand_weapons(self):
        return self.filter_by_type('TwoHand')


    def filter_by_type(self, weapon_type):
        f = (lambda w: w.is_weapon_type([weapon_type]))
        return list(filter(f, self.weapons))

    
    def get_weapon_by_name(self, weapon_name):
        if not weapon_name in self.weapon_dict.keys():
            return None
        w = self.weapon_dict[weapon_name]
        return w


    def __repr__(self):
        return '\n'.join([f'Mainhand: {str(self.get_mainhand_weapons())}',
                          f'Offhand: {str(self.get_offhand_weapons())}',
                          f'TwoHand: {str(self.get_twohand_weapons())}'])