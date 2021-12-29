class Weapon:
    # KEY_NAMES = ['specialization', 'flags', 'skills']

    def __init__(self, name, data):
        self.name = name
        if 'specialization' in data:
            self.specialization = data['specialization']
        else:
            self.specialization = None
        self.flags = data['flags']
        self.skills = data['skills']
    

    def parse_flags(self):
        for flag in self.flags:
            print(flag)


    def __repr__(self):
        return self.name