class DamageSim:
  
  def __init__(self, player, target):
    self.player = player
    self.target = target
  

  def sim_skill(self, skill_id):
    ## (Weapon strength * Power * Skill coefficient) / Armor
    ## Strike damage
    weapon_strength = self.player.get_weapons()
    power = self.player.get_stats()['Power']
    skill_coefficient = skill_id['Coefficient']
    armor = self.target['Armor']

    strike_damage = (weapon_strength * power * skill_coefficient) / armor

    self.update_conditions(skill_id)

    return strike_damage
    

  def __repr__(self):
    return '\n'.join([
      f'Player Name: {self.player}',
      f'Target Name: {self.target}'])


sim = DamageSim('ninya', 'golem')

print(sim)