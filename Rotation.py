import copy
import hashlib
import json

class State:
    def __init__(self, skills, duration):
        self.skills = skills
        self.cds = {action: 0 for action in skills}
        self.duration = duration
    
    
    def __repr__(self):
        return str(self.cds)

    
    def __hash__(self):
        return hashlib.md5(json.dumps({s.name: self.cds[s] for s in self.cds}, sort_keys=True).encode()).hexdigest()


    def copy(self):
        return copy.deepcopy(self)
    

    def use_skill(self, skill):
        if self.cds[skill] <= 0:
            self.cds[skill] = skill.cast_time + skill.cooldown

    
    def decr_cds(self, dur):
        self.cds = {s: self.cds[s] - dur for s in self.cds}
        self.clear_cds()

    def incr_cds(self, dur):
        return {s: self.cds[s] + dur for s in self.cds}

    
    def clear_cds(self):
        self.cds = {s: max(self.cds[s], 0) for s in self.cds}


class Skill():
    def __init__(self, name, cast_time, cooldown, damage):
        self.name = name
        self.cast_time = cast_time
        self.cooldown = cooldown
        self.damage = damage
    
    def __repr__(self):
        return self.name
    
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.__str__())
        

def n_dur_rotation(skills, n=10):
    r = State(skills, n)
    return r


def use_skill(state, skill):
    new_state = state.copy()
    if new_state.cds[skill] <= 0:
        new_state.cds[skill] = skill.cast_time + skill.cooldown
    return new_state


stab = Skill('Stab', 1, 0, 5)
jab = Skill('Jab', 0.5, 3, 25)
lunge = Skill('Lunge', 1.5, 15, 75)
poke = Skill('Poke', 0.25, 5, 35)
glare = Skill('Glare', 0, 15, 40)
skills = [stab, jab, lunge, poke, glare]


if __name__ == '__main__':
    r = n_dur_rotation(skills)
    print(r)
    r.use_skill(lunge)
    print(r)
    r.cds = r.decr_cds(5)
    r.cds = r.clear_cds()
    print(r)