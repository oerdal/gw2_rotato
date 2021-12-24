import random
from Rotation import Skill, n_dur_rotation, use_skill

class Player():
    def __init__(self):
        self.rotation = []
        self.total_dmg = 0
        self.last_skill = None
        self.miscast = False
    
        self.Q = {}
        self.R = {}

        stab = Skill('Stab', 1, 0, 5)
        jab = Skill('Jab', 0.5, 3, 25)
        lunge = Skill('Lunge', 1.5, 15, 75)
        poke = Skill('Poke', 0.25, 5, 35)
        glare = Skill('Glare', 0, 15, 40)
        skills = [stab, jab, lunge, poke, glare]

        self.state = n_dur_rotation(skills)
        self.skills = self.state.skills
        print(self.state)

    def QLearn(self, gamma=.9, epochs=5, epsilon=.9, alpha=.5):
        for i in range(epochs):
            print(f'=== Epoch {i+1} ===')

            has_rewards = self.state.__hash__() in self.R
            if not has_rewards:
                self.R[self.state.__hash__()] = []
            for skill in self.skills:
                if not (self.state.__hash__(), skill) in self.Q.keys():
                    self.Q[(self.state.__hash__(), skill)] = 0
                if not has_rewards:
                    self.R[self.state.__hash__()].append(self.reward(self.state, skill))
            
            # randomly choose between the 'optimal' skill or a random skill
            # epsilon represents the probability of using a random skill
            explore_randomly = random.uniform(0, 1.0)
            if explore_randomly > epsilon:
                print('choosing the best skill')
                for skill in self.skills:
                    print(f'skill: {skill} was used. gives q value of {self.Q[(self.state.__hash__(), skill)]}')

                max_q = -10000
                best_skill = None
                for skill in self.skills:
                    if self.Q[(self.state.__hash__(), skill)] > max_q:
                        max_q = self.Q[(self.state.__hash__(), skill)]
                        best_skill = skill
                
                print(f'best skill: {best_skill} | q value: {max_q}')
                self.rotation.append(best_skill)

                # update q values
                # Q' = Q + alpha*(R + gamma*maxQ' - Q)
                for skill in self.skills:
                    Q_curr = self.Q[(self.state.__hash__(), skill)]
                    self.Q[(self.state.__hash__(), skill)] = Q_curr + alpha*(self.reward(self.state, skill) + gamma*self.max_reward(self.state, skill) - Q_curr)

                self.state = use_skill(self.state, best_skill)
                self.state.decr_cds(best_skill.cast_time)
            else:
                print('using a random skill')

                random_skill = random.choice(self.skills)
                print(f'random skill: {random_skill} | q value: {self.Q[(self.state.__hash__(), skill)]}')
                self.rotation.append(random_skill)

                # update q values
                # Q' = Q + alpha*(R + gamma*maxQ' - Q)
                for skill in self.skills:
                    Q_curr = self.Q[(self.state.__hash__(), skill)]
                    self.Q[(self.state.__hash__(), skill)] = Q_curr + alpha*(self.reward(self.state, skill) + gamma*self.max_reward(self.state, skill) - Q_curr)

                self.state = use_skill(self.state, random_skill)
                self.state.decr_cds(random_skill.cast_time)
            
            
        # print(self.Q)
        print(self.rotation)
                
    
    def reward(self, state, skill):
        reward = 0
        if state.cds[skill] <= 0:
            reward += skill.damage
        else:
            reward -= 1
        return reward
    
    
    # maximum possible reward obtainable out of all actions usable in new state
    def max_reward(self, state, skill):
        new_state = use_skill(state, skill)
        if not new_state.__hash__() in self.R:
            self.R[new_state.__hash__()] = []
            for skill in self.skills:
                self.R[new_state.__hash__()].append(self.reward(new_state, skill))
        return max(self.R[new_state.__hash__()])



p = Player()
p.QLearn(epsilon=.9, epochs=1000)