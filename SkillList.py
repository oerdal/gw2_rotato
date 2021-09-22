import Skill

class SkillList:
    def __init__(self, skills):
        self.cached_skills = {}
        skill_list = []

        for skill in skills:
            if skill in self.cached_skills:
                skill_list.append(self.cached_skills[skill])
            else:
                curr = Skill.Skill(skill)
                skill_list.append(curr)
                self.cached_skills[skill] = curr

        self.skill_list = skill_list
    
    def __repr__(self):
        repr = ''
        
        for S in self.skill_list:
            repr += S.skill_name + ', '
        
        repr = repr.rstrip(', ')
        return repr
