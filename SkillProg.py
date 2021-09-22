import Skill

def main():
    usr_skill_name = input('Enter a Skill Name: ')
    usr_skill = Skill.Skill(usr_skill_name)
    print(usr_skill)

if __name__ == '__main__':
    main()