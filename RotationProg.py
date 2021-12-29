import sys
import base64
import requests

# [&DQEQOw0aPjpLF0sXNgF6FlMXAABHAQAANwEAAAAAAAAAAAAAAAAAAAAAAAA=]
def main():
    if len(sys.argv) > 1:
        build_link = sys.argv[1]
    else:
        print('Enter a Build Chat Link:')
        build_link  = input()
    build_link = '[&DQEQOw0aPjpLF0sXNgF6FlMXAABHAQAANwEAAAAAAAAAAAAAAAAAAAAAAAA=]'
    print(build_link)
    decoded_build = base64.b64decode(build_link)
    build_hex = decoded_build.hex()
    build_arr = [build_hex[i:i+2] for i in range(len(build_hex)) if i%2==0]

    for i in range(2, 7, 2):
        spec = get_specializations(build_arr[i])
        if spec:
            traits = get_traits(build_arr[i+1], spec)
            print(spec['name'], [t['name'] for t in traits])
    
    


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
