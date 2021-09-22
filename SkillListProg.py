import sys
import SkillList as SKL

def main():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = './sample_rotation.txt'

    with open(file_name) as f:
        read_data = f.read()
    
    sample_rotato = read_data.split('\n')
    skl = SKL.SkillList(sample_rotato)
    print(skl)

if __name__ == '__main__':
    main()