class WeaponSkill():
  
  def __init__(self, skill_json):
    self.skill_name = skill_json['name']
    self.id = skill_json['id']
    self.icon = skill_json['icon']